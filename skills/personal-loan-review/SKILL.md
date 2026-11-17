---
name: personal-loan-review
description: How to apply the sample personal_loan policy pack and sample application folder.
---

# Personal loan review

Sample pack: `/applications/sample-personal-loan` against product `personal_loan`.

Policy YAML: `/policies/personal_loan.yaml`  
Narrative: `/policies/personal_loan.md`

## What to compute

- `amortizing_payment` from requested amount, annual rate (decimal), term months
- `dti` = (housing + other monthly debt + proposed payment) / monthly gross income
- `residual_income` when net income exists
- Skip using `ltv` / `dscr` as pass/fail; they are stubs for later products

## Typical sample borrower

Jordan Hale, $18,000 / 36 months / 11.9%, FICO 732, income and debts that should clear 43% DTI if documents match.
