"""Write a synthetic personal-loan package under data/applications/sample-personal-loan."""

from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from underwriting_agent.config import APPLICATIONS_DIR  # noqa: E402
from underwriting_agent.simple_pdf import write_simple_pdf  # noqa: E402

OUT = APPLICATIONS_DIR / "sample-personal-loan"


def write_application_docx(path: Path) -> None:
    doc = Document()
    title = doc.add_paragraph("Unsecured Personal Loan Application")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rows = [
        ("Applicant name", "Jordan Hale"),
        ("Date of birth", "1988-04-12"),
        ("Address", "410 Maple Street, Portland, OR 97201"),
        ("Employer", "Northline Analytics LLC"),
        ("Job title", "Operations analyst"),
        ("Employment start date", "2023-06-01"),
        ("Employment tenure months", "28"),
        ("Monthly gross income", "7200"),
        ("Monthly net income", "5400"),
        ("Monthly rent", "1600"),
        ("Monthly auto loan", "350"),
        ("Requested amount", "18000"),
        ("Term months", "36"),
        ("Annual interest rate", "0.119"),
        ("Purpose", "Debt consolidation"),
        ("Bankruptcy in last 24 months", "No"),
    ]
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Field"
    table.rows[0].cells[1].text = "Value"
    for field, value in rows:
        cells = table.add_row().cells
        cells[0].text = field
        cells[1].text = value
    doc.add_paragraph("I certify that the information on this application is true and complete.")
    doc.add_paragraph("Applicant signature: Jordan Hale")
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


def write_sample_package(out: Path = OUT) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    write_application_docx(out / "loan_application.docx")
    write_simple_pdf(
        out / "government_id.pdf",
        [
            "STATE OF OREGON\nDRIVER LICENSE\nName: Jordan Hale\nDOB: 1988-04-12\n"
            "Address: 410 Maple Street, Portland, OR 97201\nID No: DL-OR-883194"
        ],
    )
    write_simple_pdf(
        out / "pay_stub_current.pdf",
        [
            "Northline Analytics LLC\nPay stub period: 2026-09-16 to 2026-09-30\n"
            "Employee: Jordan Hale\nGross pay this period: 3600.00\n"
            "Year to date gross: 64800.00\nMonthly gross equivalent: 7200.00\n"
            "Net pay this period: 2700.00"
        ],
    )
    write_simple_pdf(
        out / "pay_stub_prior.pdf",
        [
            "Northline Analytics LLC\nPay stub period: 2026-09-01 to 2026-09-15\n"
            "Employee: Jordan Hale\nGross pay this period: 3600.00\n"
            "Year to date gross: 61200.00\nMonthly gross equivalent: 7200.00"
        ],
    )
    write_simple_pdf(
        out / "bank_statement.pdf",
        [
            "Cascade Credit Union - Statement\nAccount holder: Jordan Hale\n"
            "Period: 2026-09-01 to 2026-09-30\nEnding balance: 11240.55\n"
            "Direct deposit Northline Analytics 3600.00 on 2026-09-15\n"
            "Direct deposit Northline Analytics 3600.00 on 2026-09-30"
        ],
    )
    write_simple_pdf(
        out / "credit_summary.pdf",
        [
            "Consumer credit snapshot (synthetic)\nName: Jordan Hale\n"
            "FICO score: 732\nRevolving utilization: 18%\n"
            "Open auto loan monthly payment: 350.00\n"
            "Bankruptcy public records last 24 months: None"
        ],
    )
    (out / "README.md").write_text(
        "# Sample personal loan file\n\n"
        "Synthetic borrower **Jordan Hale**. Drop-in path for Studio:\n\n"
        "> Underwrite `/applications/sample-personal-loan` against `personal_loan`.\n",
        encoding="utf-8",
    )
    return out


if __name__ == "__main__":
    written = write_sample_package()
    print(f"Wrote sample application to {written}")
