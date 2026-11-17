from underwriting_agent.tools.calculations import (
    amortizing_payment_amount,
    dscr,
    dti_ratio,
    ltv,
    residual_income_amount,
)


def test_zero_rate_payment_splits_principal() -> None:
    assert amortizing_payment_amount(1200, 0.0, 12) == 100.0


def test_known_amortizing_payment() -> None:
    payment = amortizing_payment_amount(18_000, 0.119, 36)
    assert payment == 597.0


def test_dti_includes_proposed_payment() -> None:
    ratio = dti_ratio(1600 + 350 + 597.0, 7200)
    assert ratio == 0.3538


def test_residual_income() -> None:
    assert residual_income_amount(5400, 1600 + 350 + 597.0) == 2853.0


def test_ltv_stub_not_used_by_personal_loan() -> None:
    result = ltv.invoke({"loan_amount": 80_000, "collateral_value": 100_000})
    assert result["ltv"] == 0.8
    assert result["used_by_personal_loan"] is False
    assert "not used by personal_loan" in result["note"]


def test_dscr_stub_not_used_by_personal_loan() -> None:
    result = dscr.invoke({"net_operating_income": 120_000, "annual_debt_service": 80_000})
    assert result["dscr"] == 1.5
    assert result["used_by_personal_loan"] is False
