---
name: cv-tailoring-guard
description: >-
  Enforce strict fact verification, LaTeX compilation integrity, page budgeting,
  and ATS text-layer checks for the Module 2 (Apply) CV tailoring pipeline.
---

# CV Tailoring Guard

Use this skill when developing, testing, or reviewing code in `backend/app/services/cv_tailor/` or modifying `cv_templates/`.

## Non-Negotiable Rules

### 1. Never Invent Facts
- `01_MASTER_CV.tex` (or whichever template is active) is the **exclusive source of truth** for a user's experience.
- The tailoring pipeline may reorder bullets, trim lower-relevance items, rewrite the Summary section using facts from the file, and mirror keywords from the job description *only where truthful*.
- **Verified Fact Ledger** from `01_MASTER_CV.tex`:
  - `600+ salespersons` (Betopia Sales Agent)
  - `530+ problems` = `350+ LeetCode` + `200+ Codeforces`
  - `32,247 matches, 1990--2025` (FIFA forecast)
  - `10,000+ fights, 80+ features, sub-100ms` (UFC)
  - `28,000+ listings, 95%+ accuracy` (rent prediction)
  - `97% average accuracy` (crop disease)
  - `sub-100ms inference latency` (Softvence FastAPI APIs)
  - `6-month, 1-year, 5-year horizons` (BioVue)
  - `Betopia Limited, AI Engineer: Apr 2026 -- Present`
  - `Softvence Agency, AI Developer: Nov 2025 -- Mar 2026`
  - `B.Sc. ICE, University of Rajshahi: Jan 2019 -- Oct 2024`
- If a job demands a skill or credential not in the source file, it must be flagged as a gap in the review pass — **never hallucinated or inferred**.

### 2. LaTeX Syntax & Preamble Preservation
- Keep everything from `\documentclass` through `\begin{document}` (preamble, packages, custom macros) **exactly as-is**.
- Control blocks (lines starting with `%%`) must be stripped from generated output.
- Escape LaTeX special characters (`%`, `&`, `$`, `#`, `_`, `^`, `{`, `}`) in any generated text.

### 3. Relevance-Weighted Trimming & Page Budget
- Target: 1 page. Hard limit: 2 pages max.
- Use relevance-weighted line scoring:
  `score = relevance_to_posting + uniqueness_in_document + cover_letter_dependency`
- Default trim fallback sequence:
  1. Robotics & Embedded projects (unless the posting is for embedded/robotics)
  2. Certifications & Courses
  3. Career Highlights
  4. Technical Leadership & Ownership
  5. Enterprise AI Systems duplicates
  6. Lower-relevance personal projects

### 4. PDF Verification & ATS Text-Layer Check
- Compile with `lualatex` or `pdflatex`.
- Extract text layer using `pdftotext` or `pypdf` to verify:
  - Header contact details exist as plain parseable text.
  - No garbled characters or ligatures.
  - Page count does not exceed limit.
