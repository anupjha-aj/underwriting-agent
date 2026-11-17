from pathlib import Path

from docx import Document

from underwriting_agent.simple_pdf import write_simple_pdf
from underwriting_agent.tools.documents import extract_document_markdown


def test_pdf_extract_has_page_markers(tmp_path: Path) -> None:
    pdf = tmp_path / "income.pdf"
    write_simple_pdf(pdf, ["Gross monthly income 7200", "Page two leftover"])
    markdown = extract_document_markdown(pdf)
    assert "## Page 1" in markdown
    assert "Gross monthly income 7200" in markdown
    assert "## Page 2" in markdown


def test_docx_extract_has_paragraph_and_table_markers(tmp_path: Path) -> None:
    path = tmp_path / "application.docx"
    doc = Document()
    doc.add_paragraph("Unsecured Personal Loan Application")
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Requested amount"
    table.rows[0].cells[1].text = "18000"
    doc.save(path)
    markdown = extract_document_markdown(path)
    assert "## Paragraph 1" in markdown
    assert "Unsecured Personal Loan Application" in markdown
    assert "## Table 1 Row 1" in markdown
    assert "18000" in markdown
