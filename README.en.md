# Amazon written-review collection and insight

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Use the user's explicitly requested output language; otherwise follow the request language. Keep commands, skill IDs, JSON keys, enum values, units and source quotations unchanged. Separate translations from originals. Never infer country, currency or jurisdiction from language. Read the relevant detailed references in the complete specification and retain all existing validation and authorization gates.

## Installation and use

Download or clone the repository and copy the indicated skill directory, including its existing references, scripts, assets and other dependencies, into your host's skill directory. Keep its name and SKILL.md. Changing the documentation language does not require another installation. Commands are installation options, not evidence of installation or activation.

```sh
git clone https://github.com/PDBen-Auto/amazon-review-intelligence-skill.git
```

## Amazon written-review collection and insight

`amazon-review-scraper`

Collect or analyze written reviews for exact ASINs, conservatively deduplicate and deliver traceable workbooks and offline insight reports.

Skill directory: `.`

**Implementation Basis and Dependencies**

Python 3.10+ for scripts; openpyxl for XLSX, optional Pillow for embedded images. Woot is optional and US-only with exact offer/ASIN matching; other markets need an available authorized connector or browser.

**Inputs**

Collection: ASINs/URLs and marketplace, optional date/star/count filter. Analysis-only: supplied JSON/CSV/XLSX/HTML. Specify deliverables and privacy permissions; existing complete files do not require another scrape.

**Outputs**

Per-ASIN source/status records, canonical JSON, requested XLSX/CSV/media URLs, offline HTML and optional VOC/evidence handoff. Retain full original text separately from translation and summary.

[Workflow · Boundaries and stopping conditions · Example request](references/i18n/en.md)

> Use `$amazon-review-scraper` — Analyze supplied mount reviews, keep originals, explain recurring problems in the requested language and show sample limits instead of claiming a true failure rate; respond in English and preserve evidence, unknowns and action boundaries.

## Language coverage and validation

This localized operating guide covers purpose, prerequisites, inputs, outputs, workflow, examples and boundaries; it is not a line-by-line translation of every reference. Detailed technical references, historical cases, script errors, example interfaces and images retain their original language. The assistant can explain them in the requested language. Structural, link and key-constraint checks are performed; native-speaker editorial review for each language is not claimed.

Before delivery reconcile inputs, evidence, missing values, files and the original completion criteria. Mark unexecuted steps unverified; a successful script exit is not business validation.
