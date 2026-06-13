from pathlib import Path

import fitz
from docx import Document


def extract_text(path: Path, content_type: str) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf" or content_type == "application/pdf":
        return _extract_pdf(path)
    if suffix == ".docx" or "wordprocessingml" in content_type:
        return _extract_docx(path)
    raise ValueError(f"Unsupported resume format: {path.name}")


def _extract_pdf(path: Path) -> str:
    with fitz.open(path) as doc:
        return "\n".join(page.get_text("text") for page in doc)


def _extract_docx(path: Path) -> str:
    document = Document(path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
