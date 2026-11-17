import pytest

from underwriting_agent.config import APPLICATIONS_DIR, resolve_virtual_path


def test_resolve_applications_path() -> None:
    resolved = resolve_virtual_path("/applications/sample-personal-loan/loan_application.docx")
    assert resolved == APPLICATIONS_DIR / "sample-personal-loan" / "loan_application.docx"


def test_resolve_rejects_escape() -> None:
    with pytest.raises(ValueError, match="escapes"):
        resolve_virtual_path("/applications/../policies/personal_loan.yaml")


def test_resolve_unknown_prefix() -> None:
    with pytest.raises(ValueError, match="Unsupported"):
        resolve_virtual_path("/etc/passwd")
