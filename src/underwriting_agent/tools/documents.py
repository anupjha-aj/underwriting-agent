"""Parse uploaded PDF and DOCX files into cited text sidecars."""

from __future__ import annotations

from pathlib import Path

from langchain.tools import tool
from pypdf import PdfReader

from underwriting_agent.config import WORKSPACE_DIR, resolve_virtual_path


def extract_pdf_markdown(path: Path) -> str:
    reader = PdfReader(str(path))
    pages: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        pages.append(f"## Page {index}\n\n{text or '[no extractable text]'}")
    return f"# Extracted from {path.name}\n\n" + "\n\n".join(pages)


def extract_docx_markdown(path: Path) -> str:
    from docx import Document

    document = Document(str(path))
    sections: list[str] = [f"# Extracted from {path.name}"]
    for index, paragraph in enumerate(document.paragraphs, start=1):
        text = paragraph.text.strip()
        if text:
            sections.append(f"## Paragraph {index}\n\n{text}")
    for table_index, table in enumerate(document.tables, start=1):
        for row_index, row in enumerate(table.rows, start=1):
            cells = " | ".join(cell.text.strip() for cell in row.cells)
            if cells.strip(" |"):
                sections.append(f"## Table {table_index} Row {row_index}\n\n{cells}")
    if len(sections) == 1:
        sections.append("## Paragraph 1\n\n[no extractable text]")
    return "\n\n".join(sections)


def extract_document_markdown(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_markdown(path)
    if suffix == ".docx":
        return extract_docx_markdown(path)
    raise ValueError(f"Unsupported file type {suffix!r}. Ingest PDF or DOCX only.")


def write_extracted_sidecar(source: Path, markdown: str) -> Path:
    extracted_dir = WORKSPACE_DIR / "extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)
    sidecar = extracted_dir / f"{source.stem}.md"
    sidecar.write_text(markdown, encoding="utf-8")
    return sidecar


@tool
def ingest_document(path: str) -> str:
    """Extract text from a PDF or DOCX under /applications/ with page or paragraph markers.

    Writes a sidecar markdown file to /workspace/extracted/{stem}.md for citation.
    Use this before classifying or extracting financial facts. Binary originals
    cannot be read with read_file.
    """
    resolved = resolve_virtual_path(path)
    if not resolved.is_file():
        return f"Error: file not found: {path}"
    try:
        markdown = extract_document_markdown(resolved)
    except ValueError as exc:
        return f"Error: {exc}"
    sidecar = write_extracted_sidecar(resolved, markdown)
    virtual_sidecar = f"/workspace/extracted/{sidecar.name}"
    return (
        f"Ingested {path}\n"
        f"Extracted text written to {virtual_sidecar}\n\n"
        f"{markdown}"
    )
