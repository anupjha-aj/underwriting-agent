---
name: citation-and-evidence
description: Quote-or-do-not-claim rules for underwriting facts and policy results.
---

# Citation and evidence

Every material number in a credit decision needs a `SourceRef`:

- `file_path` — virtual path (`/applications/...` or `/workspace/extracted/...`)
- `page` for PDFs (from `## Page N` headings)
- `paragraph` for DOCX (from `## Paragraph N` headings)
- `quote` — a short verbatim excerpt

If you cannot quote it, do not claim it. Put an `Issue` of type `question` or `missing_document` instead.

Do not compute DTI or payment in prose; copy the tool JSON into metrics.
