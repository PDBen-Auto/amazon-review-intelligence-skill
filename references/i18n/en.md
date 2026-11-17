# Amazon written-review collection and insight

`amazon-review-scraper` · English

## Purpose and scope

Collect or analyze written reviews for exact ASINs, conservatively deduplicate and deliver traceable workbooks and offline insight reports.

## Implementation Basis and Dependencies

Python 3.10+ for scripts; openpyxl for XLSX, optional Pillow for embedded images. Woot is optional and US-only with exact offer/ASIN matching; other markets need an available authorized connector or browser.

## Inputs

Collection: ASINs/URLs and marketplace, optional date/star/count filter. Analysis-only: supplied JSON/CSV/XLSX/HTML. Specify deliverables and privacy permissions; existing complete files do not require another scrape.

## Outputs

Per-ASIN source/status records, canonical JSON, requested XLSX/CSV/media URLs, offline HTML and optional VOC/evidence handoff. Retain full original text separately from translation and summary.

## Workflow

1. Resolve target and market.
2. Verify exact Woot mapping or authorized fallback.
3. Treat interface zero and partial pages as inconclusive.
4. Merge by stable ID or complete-text evidence.
5. Assign one primary issue/benefit per review
6. secondary tags do not form an exclusive denominator.
7. Build, reopen and reconcile requested files.

## Boundaries and stopping conditions

Stop on CAPTCHA, login wall or access restrictions. No cookies, orders or account data. Escape HTML/formulas. Written reviews differ from ratings; a review sample does not prove population defect rate. Fixed translation_zh/summary_zh schema fields remain Chinese.

## Example request

Use `$amazon-review-scraper` — Analyze supplied mount reviews, keep originals, explain recurring problems in the requested language and show sample limits instead of claiming a true failure rate; respond in English and preserve evidence, unknowns and action boundaries.

## Complete specification

[Skill entrypoint and detailed references](../../SKILL.md).

Use the user's explicitly requested output language; otherwise follow the request language. Keep commands, skill IDs, JSON keys, enum values, units and source quotations unchanged. Separate translations from originals. Never infer country, currency or jurisdiction from language. Read the relevant detailed references in the complete specification and retain all existing validation and authorization gates.

Before delivery reconcile inputs, evidence, missing values, files and the original completion criteria. Mark unexecuted steps unverified; a successful script exit is not business validation.

## Language coverage and validation

This localized operating guide covers purpose, prerequisites, inputs, outputs, workflow, examples and boundaries; it is not a line-by-line translation of every reference. Detailed technical references, historical cases, script errors, example interfaces and images retain their original language. The assistant can explain them in the requested language. Structural, link and key-constraint checks are performed; native-speaker editorial review for each language is not claimed.

