"""Structured underwriting outputs with source citations."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class Recommendation(StrEnum):
    approve = "approve"
    decline = "decline"
    refer = "refer"


class DocumentType(StrEnum):
    application = "application"
    government_id = "government_id"
    pay_stub = "pay_stub"
    bank_statement = "bank_statement"
    tax_return = "tax_return"
    employment_letter = "employment_letter"
    credit_report = "credit_report"
    other = "other"


class IssueType(StrEnum):
    missing_document = "missing_document"
    inconsistency = "inconsistency"
    question = "question"


class Severity(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"


class SourceRef(BaseModel):
    file_path: str
    page: int | None = Field(default=None, description="1-based PDF page number")
    paragraph: int | None = Field(default=None, description="1-based DOCX paragraph index")
    quote: str = Field(description="Exact excerpt supporting the claim")


class ClassifiedDocument(BaseModel):
    file_path: str
    document_type: DocumentType
    borrower_role: Literal["primary", "co_borrower", "unknown"] = "primary"
    completeness_notes: str = ""


class DocumentIntakeResult(BaseModel):
    documents: list[ClassifiedDocument]
    checklist_notes: str = ""


class FinancialFact(BaseModel):
    field: str = Field(
        description=(
            "Canonical field such as stated_income, monthly_debt, liquid_assets, "
            "fico, requested_amount, term_months, annual_rate, employment_tenure_months"
        )
    )
    value: str
    unit: str = Field(default="", description="USD, percent, months, score, etc.")
    source: SourceRef
    confidence: float = Field(ge=0.0, le=1.0)


class FinancialExtractionResult(BaseModel):
    facts: list[FinancialFact]


class Issue(BaseModel):
    issue_type: IssueType
    severity: Severity
    summary: str
    evidence: list[SourceRef] = Field(default_factory=list)


class GapAnalysisResult(BaseModel):
    issues: list[Issue]


class PolicyResult(BaseModel):
    rule_id: str
    passed: bool
    summary: str
    evidence: list[SourceRef] = Field(default_factory=list)


class CalculatedMetrics(BaseModel):
    proposed_monthly_payment: float | None = None
    dti: float | None = None
    residual_income: float | None = None
    ltv: float | None = None
    dscr: float | None = None
    notes: list[str] = Field(default_factory=list)


class CreditPolicyResult(BaseModel):
    product_id: str
    metrics: CalculatedMetrics
    policy_results: list[PolicyResult]
    proposed_recommendation: Recommendation
    rationale: str


class CreditDecision(BaseModel):
    """Final underwriting recommendation for the lending team."""

    recommendation: Recommendation
    product_id: str
    metrics: CalculatedMetrics
    policy_results: list[PolicyResult]
    issues: list[Issue]
    rationale: str
    evidence: list[SourceRef] = Field(default_factory=list)
