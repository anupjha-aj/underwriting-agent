from underwriting_agent.tools.policy import load_policy_dict, load_products_index


def test_default_product_is_personal_loan() -> None:
    index = load_products_index()
    assert index["default_product"] == "personal_loan"
    assert "personal_loan" in index["products"]


def test_personal_loan_limits_and_required_docs() -> None:
    policy = load_policy_dict("personal_loan")
    assert policy["limits"]["max_dti"] == 0.43
    assert policy["limits"]["min_fico"] == 660
    assert policy["limits"]["max_amount"] == 50_000
    sets = policy["required_document_sets"]
    assert ["application"] in sets
    assert ["pay_stub", "tax_return"] in sets
    assert policy["policy_file"] == "/policies/personal_loan.yaml"
    assert policy["narrative_file"] == "/policies/personal_loan.md"
