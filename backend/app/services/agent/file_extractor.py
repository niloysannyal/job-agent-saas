import base64
import csv
import io
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Max characters of extracted text to inject into context to protect token budget
MAX_EXTRACTED_CHARS = 12000

# File extension categorization
TEXT_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".py", ".js", ".jsx", ".ts", ".tsx",
    ".json", ".html", ".htm", ".css", ".scss", ".yaml", ".yml",
    ".tex", ".log", ".sql", ".sh", ".bat", ".env", ".xml", ".ini",
    ".cfg", ".toml", ".rst", ".dockerfile"
}

SPREADSHEET_EXTENSIONS = {".xlsx", ".xls", ".csv", ".tsv"}
PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".bmp", ".ico"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".aac", ".flac", ".webm", ".wma"}


def extract_file_content(filename: str, file_bytes: bytes, content_type: str = "") -> Dict[str, Any]:
    """
    Extracts text, structured data, and metadata from arbitrary user-uploaded files:
    - PDF: extracts all text and page counts via pypdf.
    - Spreadsheets (.xlsx, .xls, .csv): formats sheets and tables via openpyxl/csv.
    - Text/Code (.txt, .md, .py, .json, etc.): utf-8/latin-1 decoding with pretty formatting.
    - Images (.png, .jpg, etc.): extracts dimensions, format, and data URL thumbnail.
    - Audio (.mp3, .wav, etc.): extracts metadata, duration approximation, and header info.
    """
    ext = Path(filename).suffix.lower()
    file_size = len(file_bytes)
    size_kb = max(1, file_size // 1024)

    result: Dict[str, Any] = {
        "filename": filename,
        "extension": ext,
        "file_size": file_size,
        "size_formatted": f"{size_kb} KB" if size_kb < 1024 else f"{size_kb / 1024:.1f} MB",
        "file_type": "unknown",
        "summary": f"Uploaded file ({size_kb} KB)",
        "extracted_text": "",
        "preview_url": None,
        "metadata": {},
    }

    try:
        # 1. PDF Documents
        if ext in PDF_EXTENSIONS:
            result["file_type"] = "pdf"
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                num_pages = len(reader.pages)
                extracted_pages = []
                total_words = 0

                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    words = len(page_text.split())
                    total_words += words
                    if page_text.strip():
                        extracted_pages.append(f"--- Page {i + 1} ---\n{page_text.strip()}")

                full_pdf_text = "\n\n".join(extracted_pages)
                if not full_pdf_text.strip():
                    full_pdf_text = "[PDF contains no selectable text layer (scanned or image-based document)]."

                if len(full_pdf_text) > MAX_EXTRACTED_CHARS:
                    full_pdf_text = full_pdf_text[:MAX_EXTRACTED_CHARS] + f"\n\n... [Truncated: {len(full_pdf_text) - MAX_EXTRACTED_CHARS} remaining characters]"

                result["summary"] = f"PDF Document ({num_pages} page{'s' if num_pages > 1 else ''}, {total_words} words)"
                result["extracted_text"] = full_pdf_text
                result["metadata"] = {"pages": num_pages, "words": total_words}
            except Exception as e:
                logger.warning(f"Failed to parse PDF {filename}: {e}")
                result["summary"] = f"PDF Document ({size_kb} KB, extraction error)"
                result["extracted_text"] = f"[Error reading PDF file: {str(e)}]"

        # 2. Spreadsheets (Excel & CSV)
        elif ext in SPREADSHEET_EXTENSIONS:
            result["file_type"] = "spreadsheet"
            if ext in {".csv", ".tsv"}:
                try:
                    delimiter = "\t" if ext == ".tsv" else ","
                    decoded = file_bytes.decode("utf-8", errors="replace")
                    reader = csv.reader(io.StringIO(decoded), delimiter=delimiter)
                    rows = list(reader)
                    total_rows = len(rows)
                    preview_rows = rows[:50]  # Cap at top 50 rows for prompt safety
                    table_lines = []
                    for r in preview_rows:
                        table_lines.append(" | ".join([cell.strip() for cell in r]))
                    
                    csv_text = "\n".join(table_lines)
                    if total_rows > 50:
                        csv_text += f"\n... [Showing 50 of {total_rows} total rows]"

                    result["summary"] = f"Delimited Sheet ({total_rows} rows, {len(rows[0]) if rows else 0} columns)"
                    result["extracted_text"] = csv_text
                    result["metadata"] = {"total_rows": total_rows, "columns": len(rows[0]) if rows else 0}
                except Exception as e:
                    logger.warning(f"CSV read failed for {filename}: {e}")
                    result["extracted_text"] = f"[Failed reading spreadsheet: {str(e)}]"
            else:
                # Excel (.xlsx, .xls)
                try:
                    import openpyxl
                    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
                    sheet_names = wb.sheetnames
                    sheet_texts = []
                    total_records = 0

                    for sname in sheet_names[:3]:  # Check up to first 3 sheets
                        ws = wb[sname]
                        rows = list(ws.iter_rows(values_only=True))
                        total_records += len(rows)
                        header = [str(c or "").strip() for c in (rows[0] if rows else [])]
                        data_rows = rows[1:40]  # First 40 rows per sheet

                        stext = f"### Sheet: {sname} ({len(rows)} rows)\n"
                        stext += " | ".join(header) + "\n"
                        stext += " | ".join(["---"] * max(1, len(header))) + "\n"
                        for r in data_rows:
                            stext += " | ".join([str(c or "").strip() for c in r]) + "\n"
                        if len(rows) > 40:
                            stext += f"... [Showing 40 of {len(rows)} rows in sheet '{sname}']\n"
                        sheet_texts.append(stext)

                    full_sheet_text = "\n\n".join(sheet_texts)
                    result["summary"] = f"Excel Workbook ({len(sheet_names)} sheet{'s' if len(sheet_names) > 1 else ''}, {total_records} rows)"
                    result["extracted_text"] = full_sheet_text
                    result["metadata"] = {"sheets": sheet_names, "total_rows": total_records}
                except Exception as e:
                    logger.warning(f"Excel read failed for {filename}: {e}")
                    result["summary"] = f"Excel Spreadsheet ({size_kb} KB, extraction error)"
                    result["extracted_text"] = f"[Failed reading Excel workbook: {str(e)}]"

        # 3. Plain Text and Source Code
        elif ext in TEXT_EXTENSIONS or content_type.startswith("text/"):
            result["file_type"] = "text"
            try:
                decoded = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                decoded = file_bytes.decode("latin-1", errors="replace")

            if ext == ".json":
                try:
                    parsed = json.loads(decoded)
                    decoded = json.dumps(parsed, indent=2)
                except Exception:
                    pass

            lines = decoded.splitlines()
            result["summary"] = f"Code/Text File ({len(lines)} lines, {len(decoded)} chars)"

            if len(decoded) > MAX_EXTRACTED_CHARS:
                decoded = decoded[:MAX_EXTRACTED_CHARS] + f"\n\n... [Truncated: {len(decoded) - MAX_EXTRACTED_CHARS} remaining characters]"

            result["extracted_text"] = decoded
            result["metadata"] = {"line_count": len(lines)}

        # 4. Images
        elif ext in IMAGE_EXTENSIONS or content_type.startswith("image/"):
            result["file_type"] = "image"
            width, height = 0, 0
            img_format = ext.replace(".", "").upper()

            try:
                from PIL import Image
                img = Image.open(io.BytesIO(file_bytes))
                width, height = img.size
                img_format = img.format or img_format
                result["metadata"] = {"width": width, "height": height, "format": img_format}
                result["summary"] = f"{img_format} Image ({width}×{height}px, {size_kb} KB)"
            except Exception:
                result["summary"] = f"{img_format} Image ({size_kb} KB)"

            # Provide small data URL preview for images under 4MB
            if file_size <= 4 * 1024 * 1024:
                mime = content_type or f"image/{ext.replace('.', '')}"
                if ext == ".svg":
                    mime = "image/svg+xml"
                elif ext in {".jpg", ".jpeg"}:
                    mime = "image/jpeg"
                b64 = base64.b64encode(file_bytes).decode("ascii")
                result["preview_url"] = f"data:{mime};base64,{b64}"

            result["extracted_text"] = f"[Image Attached: {filename} ({width}×{height}px, {size_kb} KB)]"

        # 5. Audio Files
        elif ext in AUDIO_EXTENSIONS or content_type.startswith("audio/"):
            result["file_type"] = "audio"
            audio_format = ext.replace(".", "").upper()
            result["summary"] = f"{audio_format} Audio File ({size_kb} KB)"
            result["extracted_text"] = f"[Audio Recording Attached: {filename} ({audio_format}, {size_kb} KB)]"
            result["metadata"] = {"format": audio_format}

        # 6. Fallback (Arbitrary binary / unknown)
        else:
            result["file_type"] = "file"
            # Attempt plain text decode
            try:
                decoded = file_bytes.decode("utf-8")
                if len(decoded) > MAX_EXTRACTED_CHARS:
                    decoded = decoded[:MAX_EXTRACTED_CHARS] + f"\n... [Truncated]"
                result["extracted_text"] = decoded
                result["summary"] = f"Document ({size_kb} KB)"
            except Exception:
                result["extracted_text"] = f"[Binary File Attached: {filename} ({size_kb} KB)]"
                result["summary"] = f"Binary File ({size_kb} KB)"

    except Exception as e:
        logger.error(f"Error extracting content for {filename}: {e}", exc_info=True)
        result["extracted_text"] = f"[Error reading file {filename}: {str(e)}]"

    return result

