"""
CV Auto-Parser Service.
Extracts raw text from PDF, DOCX, TXT, or LaTeX files, and uses LLM
structured extraction to pre-fill standard candidate profile entities:
Work Experience, Education, Skills, Projects, Certifications, Contact Info, and Target Designations.
"""
import io
import json
import logging
import re
import xml.etree.ElementTree as ET
import zipfile
from typing import Any, Dict, List, Optional

import pypdf

from app.services.llm.service import LLMService

logger = logging.getLogger(__name__)


CV_EXTRACTION_SYSTEM_PROMPT = """You are an expert career data extraction system.
Your job is to parse resume/CV text into a structured, highly accurate JSON representation of the candidate's career.
You work across ALL industries and job domains (engineering, tech, product, marketing, finance, healthcare, legal, operations, etc.).

CRITICAL RULES:
1. Ground every extracted item in the actual text. NEVER invent companies, degrees, dates, or experiences.
2. Return ONLY valid, parseable JSON conforming to the requested schema. Do not include introductory or concluding remarks.
3. For skills, categorize into sensible buckets (e.g. 'Languages', 'Frameworks', 'Databases', 'Cloud & DevOps', 'Tools', 'Management', 'Soft Skills').
4. For work experience bullet points ('highlights'), capture achievement-oriented statements as an array of strings.
5. If an item (such as phone, linkedin, or gpa) is not mentioned in the text, set it to null.
"""

CV_EXTRACTION_USER_PROMPT = """Parse the following CV/Resume text into the exact JSON schema provided:

Schema:
{{
  "full_name": "string",
  "headline": "string (e.g. 'Senior Backend Engineer' or 'Financial Analyst')",
  "phone": "string or null",
  "email": "string or null",
  "summary": "string (2-4 sentence executive summary of the candidate's career)",
  "location_city": "string or null",
  "location_country": "string or null",
  "linkedin_url": "string or null",
  "github_url": "string or null",
  "portfolio_url": "string or null",
  "target_designations": ["string (3-5 suitable target job titles)"],
  "work_experiences": [
    {{
      "company": "string",
      "title": "string",
      "location": "string or null",
      "location_type": "onsite | remote | hybrid",
      "start_date": "string (e.g. '2021-06' or 'Jun 2021')",
      "end_date": "string or null (e.g. '2023-12' or 'Present' or null)",
      "is_current": boolean,
      "description": "string or null",
      "highlights": ["bullet point 1", "bullet point 2"]
    }}
  ],
  "educations": [
    {{
      "institution": "string",
      "degree": "string (e.g. 'B.Sc.', 'B.A.', 'Master', 'High School')",
      "field_of_study": "string or null (e.g. 'Computer Science', 'Business Administration')",
      "start_date": "string or null",
      "end_date": "string or null",
      "grade": "string or null (e.g. 'GPA 3.8/4.0', 'First Class')",
      "activities": "string or null"
    }}
  ],
  "skills": [
    {{
      "name": "string",
      "category": "string (e.g. 'Languages', 'Frameworks', 'Tools', 'Management')",
      "proficiency": "Beginner | Intermediate | Advanced | Expert",
      "years_of_experience": number or null
    }}
  ],
  "projects": [
    {{
      "title": "string",
      "role": "string or null",
      "url": "string or null",
      "start_date": "string or null",
      "end_date": "string or null",
      "description": "string or null",
      "highlights": ["achievement bullet 1"],
      "technologies": "string (comma-separated tech/skills used)"
    }}
  ],
  "certifications": [
    {{
      "name": "string",
      "issuing_organization": "string",
      "issue_date": "string or null",
      "expiration_date": "string or null",
      "credential_id": "string or null",
      "credential_url": "string or null"
    }}
  ]
}}

CV TEXT TO PARSE:
---------------------------------
{cv_text}
---------------------------------
"""


class CVParserService:
    """Service to extract text from CV files and structure into profile models."""

    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> str:
        """Extract plain text from PDF, DOCX, or text files."""
        fn_lower = filename.lower()
        if fn_lower.endswith(".pdf"):
            return CVParserService._extract_pdf(file_bytes)
        elif fn_lower.endswith(".docx"):
            return CVParserService._extract_docx(file_bytes)
        else:
            # Fallback to UTF-8 text decoding
            try:
                return file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                return file_bytes.decode("latin-1", errors="replace")

    @staticmethod
    def _extract_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF pages using pypdf."""
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        pages_text: List[str] = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            if txt:
                pages_text.append(txt)
        return "\n\n".join(pages_text).strip()

    @staticmethod
    def _extract_docx(file_bytes: bytes) -> str:
        """Extract text from Word .docx file by inspecting word/document.xml."""
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes)) as zf:
                xml_content = zf.read("word/document.xml")
                tree = ET.fromstring(xml_content)
                # Word XML namespace for text elements is {http://schemas.openxmlformats.org/wordprocessingml/2006/main}t
                namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                paragraphs: List[str] = []
                for p in tree.iterfind(".//w:p", namespaces):
                    texts = [node.text for node in p.iterfind(".//w:t", namespaces) if node.text]
                    if texts:
                        paragraphs.append("".join(texts))
                return "\n".join(paragraphs).strip()
        except Exception as e:
            logger.warning(f"Failed to parse docx via XML: {e}")
            return ""

    @staticmethod
    async def parse_cv_text(text: str, llm_service: LLMService) -> Dict[str, Any]:
        """Send extracted CV text to LLM to parse into structured career JSON."""
        if not text or len(text.strip()) < 20:
            raise ValueError("Extracted CV text is empty or too short to parse.")

        prompt = CV_EXTRACTION_USER_PROMPT.format(cv_text=text[:16000])  # budget token window
        raw_response = await llm_service.generate(
            prompt=prompt,
            context=CV_EXTRACTION_SYSTEM_PROMPT,
        )

        cleaned_json = CVParserService._clean_json_output(raw_response)
        try:
            parsed = json.loads(cleaned_json)
        except json.JSONDecodeError as err:
            logger.error(f"Failed to decode LLM response as JSON: {err}. Raw output:\n{raw_response}")
            raise ValueError(f"LLM returned malformed JSON: {err}")

        # Normalize arrays and nested fields
        return CVParserService._normalize_parsed_data(parsed)

    @staticmethod
    def _clean_json_output(raw: str) -> str:
        """Strip markdown fences (```json ... ```) from output."""
        cleaned = raw.strip()
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
        if match:
            return match.group(1).strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.lstrip("`").strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
        return cleaned

    @staticmethod
    def _normalize_parsed_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all required root keys exist with appropriate types and defaults."""
        return {
            "full_name": str(data.get("full_name") or "Candidate"),
            "headline": str(data.get("headline") or "Professional"),
            "phone": data.get("phone"),
            "email": data.get("email"),
            "summary": str(data.get("summary") or ""),
            "location_city": data.get("location_city"),
            "location_country": data.get("location_country"),
            "linkedin_url": data.get("linkedin_url"),
            "github_url": data.get("github_url"),
            "portfolio_url": data.get("portfolio_url"),
            "target_designations": list(data.get("target_designations") or []),
            "work_experiences": list(data.get("work_experiences") or []),
            "educations": list(data.get("educations") or []),
            "skills": list(data.get("skills") or []),
            "projects": list(data.get("projects") or []),
            "certifications": list(data.get("certifications") or []),
        }

