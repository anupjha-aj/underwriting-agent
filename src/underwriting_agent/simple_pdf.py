"""Minimal text PDF writer for samples and tests (Helvetica, ASCII)."""

from __future__ import annotations

from pathlib import Path


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _content_stream(page_text: str) -> bytes:
    lines = page_text.splitlines() or [""]
    commands = ["BT", "/F1 11 Tf", "72 720 Td"]
    for index, line in enumerate(lines):
        ascii_line = line.encode("ascii", "replace").decode("ascii")
        if index:
            commands.append("0 -16 Td")
        commands.append(f"({_escape(ascii_line[:110])}) Tj")
    commands.append("ET")
    return ("\n".join(commands) + "\n").encode("ascii")


def write_simple_pdf(path: Path, pages: list[str]) -> None:
    """Write a one-font PDF with one content stream per page."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not pages:
        pages = [""]

    page_count = len(pages)
    font_id = 3 + page_count * 2
    objects: dict[int, bytes] = {}
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{3 + i} 0 R" for i in range(page_count))
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {page_count} >>".encode("ascii")

    for i, page_text in enumerate(pages):
        page_id = 3 + i
        content_id = 3 + page_count + i
        stream = _content_stream(page_text)
        objects[page_id] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Contents {content_id} 0 R "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> >>"
        ).encode("ascii")
        objects[content_id] = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"endstream"
        )

    objects[font_id] = (
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    )

    chunks: list[bytes] = [b"%PDF-1.4\n"]
    offsets = {0: 0}
    for obj_id in range(1, font_id + 1):
        offsets[obj_id] = sum(len(chunk) for chunk in chunks)
        chunks.append(f"{obj_id} 0 obj\n".encode("ascii") + objects[obj_id] + b"\nendobj\n")

    xref_start = sum(len(chunk) for chunk in chunks)
    xref = [f"xref\n0 {font_id + 1}\n".encode("ascii"), b"0000000000 65535 f \n"]
    for obj_id in range(1, font_id + 1):
        xref.append(f"{offsets[obj_id]:010d} 00000 n \n".encode("ascii"))
    chunks.extend(xref)
    chunks.append(
        f"trailer << /Size {font_id + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode(
            "ascii"
        )
    )
    path.write_bytes(b"".join(chunks))
