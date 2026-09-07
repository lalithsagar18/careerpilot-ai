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


def assess_resume_quality(text: str) -> dict:
    """Deterministic heuristic ATS resume quality assessment."""
    if not text:
        return {
            "overall_score": 0.0,
            "structural_score": 0.0,
            "completeness_score": 0.0,
            "action_verb_score": 0.0,
            "quantified_metric_score": 0.0,
            "recommendations": ["Upload a non-empty resume document."]
        }

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    word_count = len(text.split())

    # Check structural sections
    text_lower = text.lower()
    sections_found = sum(
        1 for s in ["experience", "education", "skill", "project", "summary", "certification"]
        if s in text_lower
    )
    structural_score = min(100.0, (sections_found / 4.0) * 100.0)

    # Check action verbs
    action_verbs = [
        "architected", "built", "developed", "engineered", "led", "designed",
        "implemented", "optimized", "spearheaded", "orchestrated", "created",
        "managed", "reduced", "increased", "delivered", "deployed"
    ]
    action_verb_matches = sum(1 for v in action_verbs if re.search(r'\b' + v + r'\b', text_lower))
    action_verb_score = min(100.0, (action_verb_matches / 5.0) * 100.0)

    # Check quantified metrics (e.g., numbers, percentages, dollar amounts)
    metrics_matches = len(re.findall(r'(\d+[\.,]?\d*[%kMB\+]?|\$\d+)', text))
    quantified_metric_score = min(100.0, (metrics_matches / 6.0) * 100.0)

    # Completeness based on length & depth
    completeness_score = min(100.0, max(40.0, (word_count / 350.0) * 100.0))

    overall_score = round(
        structural_score * 0.30 +
        action_verb_score * 0.25 +
        quantified_metric_score * 0.25 +
        completeness_score * 0.20,
        1
    )

    recs = []
    if structural_score < 75:
        recs.append("Add clear standard section headings (Experience, Skills, Education, Projects).")
    if action_verb_score < 75:
        recs.append("Start accomplishment bullets with strong action verbs (e.g. Architected, Engineered, Led).")
    if quantified_metric_score < 75:
        recs.append("Include more quantified impact metrics (e.g. reduced latency by 35%, managed 10M requests).")

    return {
        "overall_score": overall_score,
        "structural_score": round(structural_score, 1),
        "completeness_score": round(completeness_score, 1),
        "action_verb_score": round(action_verb_score, 1),
        "quantified_metric_score": round(quantified_metric_score, 1),
        "recommendations": recs or ["Resume meets high ATS formatting and impact standards."]
    }

