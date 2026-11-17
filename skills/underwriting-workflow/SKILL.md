---
name: underwriting-workflow
description: Ordered loan-file review for the underwriting Deep Agent — ingest, classify, extract, gap analysis, then policy.
---

# Underwriting workflow

Use this skill whenever the user asks to underwrite, review, or credit-decide a loan file.

## Order of work

1. Confirm product_id (`personal_loan` if unspecified) via `list_products` / `load_product_policy`.
2. List `/applications/<folder>/`.
3. `ingest_document` every `.pdf` and `.docx`. Sidecars land in `/workspace/extracted/`.
4. `task` `document-intake`.
5. `task` `financial-extraction`.
6. `task` `gap-and-consistency`.
7. `task` `credit-policy` (must use calculation tools).
8. Return a Decision on if the Loan should be approved or not based on the credit policy rules and calculations done and also emit the gaps and consistencies

Do not skip ingest. Do not approve without cited required documents.
