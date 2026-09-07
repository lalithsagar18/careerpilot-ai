import io
import re
from typing import Tuple

class DocumentExtractor:
    """Safely extracts clean plain text from uploaded PDF, DOCX, and TXT files."""

    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        
        if ext == "pdf":
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                text_parts = []
                for page in doc:
                    text_parts.append(page.get_text())
                doc.close()
                raw_text = "\n".join(text_parts)
                return DocumentExtractor.sanitize_text(raw_text)
            except Exception as e:
                # Fallback simple text extraction
                return DocumentExtractor.sanitize_text(file_bytes.decode("utf-8", errors="ignore"))

        elif ext in ["docx", "doc"]:
            try:
                import docx
                doc = docx.Document(io.BytesIO(file_bytes))
                text_parts = [p.text for p in doc.paragraphs if p.text]
                for table in doc.tables:
                    for row in table.rows:
                        text_parts.append(" | ".join([cell.text.strip() for cell in row.cells if cell.text.strip()]))
                return DocumentExtractor.sanitize_text("\n".join(text_parts))
            except Exception:
                return DocumentExtractor.sanitize_text(file_bytes.decode("utf-8", errors="ignore"))

        else:
            # Default TXT / Markdown
            return DocumentExtractor.sanitize_text(file_bytes.decode("utf-8", errors="ignore"))

    @staticmethod
    def sanitize_text(text: str) -> str:
        """Removes null bytes, excessive whitespace, and potentially harmful control characters."""
        if not text:
            return ""
        # Remove null characters
        text = text.replace('\x00', '')
        # Normalize carriage returns and line feeds
        text = re.sub(r'\r\n|\r', '\n', text)
        # Collapse excessive consecutive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
