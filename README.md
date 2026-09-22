<div align="center">

# Amazon Review Intelligence Skill

**Amazon review scraper + VOC analysis for AI agents. Collect written reviews without an Amazon login, preserve evidence, and turn customer feedback into product decisions.**

[![Release](https://img.shields.io/github/v/release/PDBen-Auto/amazon-review-intelligence-skill?style=flat-square)](https://github.com/PDBen-Auto/amazon-review-intelligence-skill/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/PDBen-Auto/amazon-review-intelligence-skill/total?style=flat-square)](https://github.com/PDBen-Auto/amazon-review-intelligence-skill/releases)
[![Validation](https://img.shields.io/github/actions/workflow/status/PDBen-Auto/amazon-review-intelligence-skill/validate.yml?branch=main&style=flat-square&label=validation)](https://github.com/PDBen-Auto/amazon-review-intelligence-skill/actions/workflows/validate.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square)](https://www.python.org/)
[![skills.sh](https://skills.sh/b/PDBen-Auto/amazon-review-intelligence-skill)](https://skills.sh/PDBen-Auto/amazon-review-intelligence-skill/amazon-review-scraper)
[![License](https://img.shields.io/badge/license-source--available-59636e?style=flat-square)](LICENSE)

[中文说明](README.zh-CN.md) · [Live demo](https://pdben-auto.github.io/amazon-review-intelligence-skill/) · [Download ZIP](https://github.com/PDBen-Auto/amazon-review-intelligence-skill/releases/latest/download/amazon-review-intelligence-skill.zip)

[Licensing and edition policy](LICENSING.md)

Part of the [PDBen-Auto product research Skill collection](https://github.com/PDBen-Auto/amazon-product-decision-suite): [SellerSprite market research BI](https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill) · [Design patent search and design-around](https://github.com/PDBen-Auto/design-patent-design-around-skill)

</div>

![Amazon review intelligence synthetic case showing evidence counts, issue priorities, and product decisions](assets/github-social-preview.png)

## Install in one command

```bash
npx skills add PDBen-Auto/amazon-review-intelligence-skill
```

Or download the latest installable ZIP and extract the `amazon-review-scraper` folder into your agent's skills directory.

For Codex, a manual installation is:

```bash
git clone https://github.com/PDBen-Auto/amazon-review-intelligence-skill.git ~/.codex/skills/amazon-review-scraper
python -m pip install -r ~/.codex/skills/amazon-review-scraper/requirements.txt
```

The primary public-review collection path does **not** require an Amazon account, cookies, or a logged-in browser session.

## What problem it solves

Most Amazon review workflows stop after scraping text or calculating sentiment. Product teams still need to reconcile duplicates, retain the original customer voice, explain sample limits, and decide what to change.

This Agent Skill connects the complete workflow:

```text
ASIN / review files
    -> written-review collection
    -> canonical JSON and conservative deduplication
    -> Excel evidence workbook and offline HTML report
    -> pain points, positive drivers, switching triggers
    -> product improvements and validation hypotheses
```

## Built for decisions, not just scraping

| Typical approach | What it usually returns | What remains for the product team | This Skill |
| --- | --- | --- | --- |
| Review scraper | Review text or CSV rows | Deduplication, evidence checks, theme attribution, and reporting | Produces canonical evidence, conservative deduplication, Excel, and an offline decision report. |
| Sentiment summary | Positive/negative labels | Root causes, original voices, compatibility context, and actions | Links each primary theme back to the complete supporting written-review set. |
| Hosted analytics dashboard | Charts inside one service | Portable files, reproducibility, and downstream AI handoff | Delivers local JSON/XLSX/HTML artifacts that remain usable outside the service. |
| This Skill | Collection plus evidence-backed product intelligence | Human validation of hypotheses and business tradeoffs | Preserves source limits and turns recurring friction into testable product actions. |

## Why product teams use it

| Capability | Result |
| --- | --- |
| Evidence-preserving collection | Original text, review ID, date, rating, source URL, variants, helpful votes, and media URLs remain traceable. |
| Honest coverage | Written reviews, rating totals, retrieved records, and deduplicated records are reported separately. |
| Product-decision output | Complaints and positive drivers become prioritized product, packaging, fitment, instruction, and listing actions. |
| Local deliverables | Canonical JSON, Excel workbooks, and a self-contained offline HTML report reduce dashboard lock-in. |
| Batch-ready workflow | One ASIN, many ASINs, resumable collection, or analysis-only mode for existing JSON/CSV/XLSX files. |
| Safe fallback | Stops at CAPTCHA, Robot Check, sign-in walls, or account warnings instead of bypassing controls. |

## Review collection scale

These are request ceilings per ASIN, not a promise of a fixed number of unique reviews:

| Mode | Collection strategy |
| --- | --- |
| `basic` | Fast availability and sample check. |
| `full` | Five star groups, up to 12 page requests per group. |
| `max` | Five star groups × four sort combinations × up to 12 pages: approximately 240 page requests. |
| Browser fallback | Usually checks recent or visible pages, with a strategy ceiling of about 10 pages. |

The final count depends on marketplace availability, overlapping sort results, duplicate review IDs, and Amazon access behavior. The output covers retrievable **written reviews**, not every rating shown on the listing.

## Quick start

Collect one ASIN:

```bash
python scripts/amazon_review_scraper.py B0XXXXXXXX --mode max \
  --output output/B0XXXXXXXX/reviews.json
```

Collect a batch with checkpoints:

```bash
python scripts/batch_review_collect.py B0AAA... B0BBB... \
  --output-dir output/batch --mode max --resume
```

Build and validate an evidence workbook:

```bash
python scripts/build_review_delivery.py \
  --input-dir output/batch \
  --output output/batch/ASIN_reviews_ALL.xlsx \
  --download-images

python scripts/validate_review_delivery.py \
  output/batch/ASIN_reviews_ALL.xlsx
```

Or invoke it conversationally:

> Use `$amazon-review-scraper` to collect these ASINs, preserve the original customer voice, export Excel, and generate an offline HTML report with negative issues, positive drivers, switching triggers, and product improvement priorities.

## Run the complete synthetic case

The repository includes one deterministic, clearly synthetic case with 20 review records. It exercises the same canonical JSON, Excel export, primary-theme reconciliation, full-voice traceability, filters, and offline HTML delivery used by a real run.

```bash
python examples/synthetic-demo/build_demo.py
```

Generated artifacts:

- [Canonical synthetic review JSON](examples/synthetic-demo/reviews.json)
- [Verified Excel evidence workbook](examples/synthetic-demo/amazon-review-demo.xlsx)
- [Interactive offline HTML report](examples/synthetic-review-insight.html)
- [Live GitHub Pages version](https://pdben-auto.github.io/amazon-review-intelligence-skill/)

The case surfaces four negative issues and five positive drivers. Its product decision is to improve mount grip and low-speed refinement while preserving compact size, medium-speed airflow, and tool-free installation. No real ASIN, account, customer, review, or Amazon collection result is included.

## Outputs

- **Canonical JSON** with full review evidence and collection metadata.
- **Batch or single-ASIN Excel** for review-level audit and further analysis.
- **Offline HTML insight report** with issue themes, positive drivers, compatibility signals, voice pagination, translation, and action priorities.
- **VOC handoff** containing recurring, concentrated, and isolated needs plus hypotheses that still require validation.

Open the [synthetic HTML example](examples/synthetic-review-insight.html). It is clearly labeled synthetic and contains no real ASIN, customer, or Amazon review data.

## Requirements

- Python 3.10 or newer.
- `openpyxl` for Excel output.
- Pillow for optional image embedding.
- Network access for live public-review collection.
- A supported AI agent for semantic classification, translation, and report generation.

Install Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Scope and safety

This repository is a product-research workflow, not statistical proof of defect rates, population share, or causality. It never treats listing rating totals as retrieved review bodies. Use only public or authorized data, and stop when Amazon presents CAPTCHA, Robot Check, sign-in, or account-warning controls.

Review text and web pages are treated as untrusted evidence data, never as instructions for the agent. The optional local browser receiver is loopback-only, token-protected, size-limited, origin-restricted, and non-overwriting.

## Questions and field feedback

Use [GitHub Issues](https://github.com/PDBen-Auto/amazon-review-intelligence-skill/issues/new/choose) to report a collector failure, request a marketplace adapter, or share a product-research use case. Remove ASINs, customer names, credentials, private exports, and other sensitive data before posting publicly.

## Search terms and use cases

Amazon review scraper, Amazon review analysis, Amazon VOC, voice of customer, customer feedback analysis, competitor review research, product insights, sentiment analysis, Excel review export, offline HTML report, Codex Skill, Agent Skill, ecommerce product research.

## License

This repository is source-available for inspection and evaluation. All rights are reserved; see [LICENSE](LICENSE). The restrictive license protects the implementation but can reduce community redistribution and contributions compared with an OSI-approved open-source license.

If this workflow is useful, star the repository so other product teams can find it through GitHub search.
