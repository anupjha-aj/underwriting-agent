"""Specialized Deep Agent subagents for the underwriting workflow."""

from __future__ import annotations

from typing import Any

from underwriting_agent.models import (
    CreditPolicyResult,
    DocumentIntakeResult,
    FinancialExtractionResult,
    GapAnalysisResult,
)
from underwriting_agent.prompts import (
    CREDIT_POLICY_PROMPT,
    DOCUMENT_INTAKE_PROMPT,
    FINANCIAL_EXTRACTION_PROMPT,
    GAP_CONSISTENCY_PROMPT,
)
from underwriting_agent.tools import CREDIT_TOOLS, INTAKE_TOOLS, POLICY_TOOLS


def build_subagents() -> list[dict[str, Any]]:
    return [
        {
            "name": "document-intake",
            "description": (
                "Classify ingested application files (PDF/DOCX sidecars) and map them "
                "to the product required-document checklist."
            ),
            "system_prompt": DOCUMENT_INTAKE_PROMPT,
            "tools": INTAKE_TOOLS+POLICY_TOOLS,
            "response_format": DocumentIntakeResult,
        },
        {
            "name": "financial-extraction",
            "description": (
                "Extract income, debts, assets, FICO, loan terms, and employment facts "
                "from extracted document text with SourceRef quotes."
            ),
            "system_prompt": FINANCIAL_EXTRACTION_PROMPT,
            "tools": INTAKE_TOOLS,
            "response_format": FinancialExtractionResult,
        },
        
    

      {
            "name": "gap-and-consistency",
            "description": (
                "Identify missing documents, cross-document inconsistencies, and "
                "questions for the borrower or underwriter."
            ),
            "system_prompt": GAP_CONSISTENCY_PROMPT,
            "tools": POLICY_TOOLS,
            "response_format": GapAnalysisResult,
        },
        {
            "name": "credit-policy",
            "description": (
                "Load product YAML rules, run payment/DTI/residual-income tools, and "
                "propose approve, decline, or refer with per-rule evidence."
            ),
            "system_prompt": CREDIT_POLICY_PROMPT,
            "tools": CREDIT_TOOLS,
            "response_format": CreditPolicyResult,
        },
    ]
