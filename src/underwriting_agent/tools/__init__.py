"""Underwriting tools exposed to the Deep Agent."""

from underwriting_agent.tools.calculations import (
    amortizing_payment,
    dscr,
    dti,
    ltv,
    residual_income,
)
from underwriting_agent.tools.documents import ingest_document
from underwriting_agent.tools.policy import load_product_policy, list_products

ALL_TOOLS = [
    ingest_document,
    load_product_policy,
    list_products,
    amortizing_payment,
    dti,
    residual_income,
    ltv,
    dscr,
]

INTAKE_TOOLS = [ingest_document]
POLICY_TOOLS = [load_product_policy, list_products]
CALCULATION_TOOLS = [amortizing_payment, dti, residual_income, ltv, dscr]
CREDIT_TOOLS = [*POLICY_TOOLS, *CALCULATION_TOOLS]
