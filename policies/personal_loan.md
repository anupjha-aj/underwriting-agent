# Unsecured Personal Loan — sample credit policy

This file is underwriter narrative.

## Product

Unsecured installment loan for a consumer primary applicant. Collateral tools (`ltv`, `dscr`) are not used.

## Eligibility (illustrative)

- Amount: $1,000–$50,000
- Term: 12–60 months
- Maximum DTI including the proposed payment: 43%
- Minimum FICO when a credit summary is in file: 660
- Employment: at least 6 months with current employer
- No bankruptcy in the last 24 months

## Required documents

All of the following must be present:

1. Signed or completed loan application
2. Government ID
3. Income evidence — recent pay stubs **or** a tax return
4. Bank statement (recent)

## Decisioning

- **Approve** only when documents are complete, calculations come from tools, and every YAML rule passes with a cited quote.
- **Decline** when a rule fails on documented evidence (for example DTI above 43% or FICO below 660).
- **Refer** when the file is incomplete or a required input cannot be calculated.
