"""Deterministic credit calculations. Do not approximate these in the model."""

from __future__ import annotations

from langchain.tools import tool


def amortizing_payment_amount(principal: float, annual_rate: float, term_months: int) -> float:
    if principal <= 0:
        raise ValueError("principal must be positive")
    if term_months <= 0:
        raise ValueError("term_months must be a positive integer")
    if annual_rate < 0:
        raise ValueError("annual_rate cannot be negative")
    monthly_rate = annual_rate / 12.0
    if monthly_rate == 0:
        return round(principal / term_months, 2)
    factor = (1 + monthly_rate) ** term_months
    payment = principal * monthly_rate * factor / (factor - 1)
    return round(payment, 2)


def dti_ratio(monthly_housing_plus_debt: float, monthly_gross_income: float) -> float:
    if monthly_gross_income <= 0:
        raise ValueError("monthly_gross_income must be positive")
    if monthly_housing_plus_debt < 0:
        raise ValueError("monthly_housing_plus_debt cannot be negative")
    return round(monthly_housing_plus_debt / monthly_gross_income, 4)


def residual_income_amount(monthly_net: float, total_obligations: float) -> float:
    return round(monthly_net - total_obligations, 2)


@tool
def amortizing_payment(principal: float, annual_rate: float, term_months: int) -> dict:
    """Monthly payment for a fully amortizing installment loan.

    annual_rate is a decimal (0.119 for 11.9%), not a percent.
    """
    try:
        payment = amortizing_payment_amount(principal, annual_rate, term_months)
    except ValueError as exc:
        return {"error": str(exc)}
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "term_months": term_months,
        "monthly_payment": payment,
    }


@tool
def dti(monthly_housing_plus_debt: float, monthly_gross_income: float) -> dict:
    """Debt-to-income ratio. Include housing, existing debt, and the proposed payment."""
    try:
        ratio = dti_ratio(monthly_housing_plus_debt, monthly_gross_income)
    except ValueError as exc:
        return {"error": str(exc)}
    return {
        "monthly_housing_plus_debt": monthly_housing_plus_debt,
        "monthly_gross_income": monthly_gross_income,
        "dti": ratio,
    }


@tool
def residual_income(monthly_net: float, total_obligations: float) -> dict:
    """Monthly net income minus total obligations (including proposed payment)."""
    amount = residual_income_amount(monthly_net, total_obligations)
    return {
        "monthly_net": monthly_net,
        "total_obligations": total_obligations,
        "residual_income": amount,
    }


@tool
def ltv(loan_amount: float, collateral_value: float) -> dict:
    """Loan-to-value. Not used by the sample personal_loan product."""
    if collateral_value <= 0:
        return {
            "error": "collateral_value must be positive",
            "used_by_personal_loan": False,
            "note": "not used by personal_loan",
        }
    return {
        "loan_amount": loan_amount,
        "collateral_value": collateral_value,
        "ltv": round(loan_amount / collateral_value, 4),
        "used_by_personal_loan": False,
        "note": "not used by personal_loan",
    }


@tool
def dscr(net_operating_income: float, annual_debt_service: float) -> dict:
    """Debt service coverage ratio. Not used by the sample personal_loan product."""
    if annual_debt_service <= 0:
        return {
            "error": "annual_debt_service must be positive",
            "used_by_personal_loan": False,
            "note": "not used by personal_loan",
        }
    return {
        "net_operating_income": net_operating_income,
        "annual_debt_service": annual_debt_service,
        "dscr": round(net_operating_income / annual_debt_service, 4),
        "used_by_personal_loan": False,
        "note": "not used by personal_loan",
    }
