from pathlib import Path

from underwriting_agent.config import WORKSPACE_DIR
from underwriting_agent.simple_pdf import write_simple_pdf
from underwriting_agent.tools.documents import ingest_document, write_extracted_sidecar


def test_write_extracted_sidecar(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("underwriting_agent.tools.documents.WORKSPACE_DIR", tmp_path)
    source = tmp_path / "pay_stub.pdf"
    sidecar = write_extracted_sidecar(source, "# Extracted\n\n## Page 1\n\nGross 7200")
    assert sidecar == tmp_path / "extracted" / "pay_stub.md"
    assert "Gross 7200" in sidecar.read_text(encoding="utf-8")


def test_ingest_document_tool_roundtrip(tmp_path: Path, monkeypatch) -> None:
    apps = tmp_path / "apps"
    apps.mkdir()
    pdf = apps / "id.pdf"
    write_simple_pdf(pdf, ["Name: Jordan Hale"])
    monkeypatch.setattr("underwriting_agent.tools.documents.WORKSPACE_DIR", tmp_path / "ws")
    monkeypatch.setattr(
        "underwriting_agent.tools.documents.resolve_virtual_path",
        lambda path: pdf,
    )
    result = ingest_document.invoke({"path": "/applications/id.pdf"})
    assert "Ingested" in result
    assert "## Page 1" in result
    assert "Jordan Hale" in result
    assert (tmp_path / "ws" / "extracted" / "id.md").is_file()
    assert WORKSPACE_DIR.name == "workspace"
