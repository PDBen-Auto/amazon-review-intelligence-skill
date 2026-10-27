# Changelog

All notable public changes are documented here. Private customer workflows and unpublished collection methods are excluded.

## [1.3.0] - 2026-10-27

- Require an exact current Woot offer-to-ASIN match before US public-review collection.
- Follow Woot review cursors, preserve full review text, and distinguish complete, partial, failed, and unverified-empty captures.
- Update batch resume, Excel status reporting, source limits, request ceilings, and documentation for the verified endpoint.
- Add a synthetic endpoint regression test without live self-collection.

## [1.2.2] - 2026-09-22

- Published the signed Amazon Review Intelligence release.
- Added bilingual repository positioning, release provenance, and a synthetic review-insight preview.
- Kept collection limits and CAPTCHA/sign-in stop behavior explicit.

## [1.2.0] - 2026-09-16

- Added canonical review evidence, conservative deduplication, Excel delivery, and offline HTML reporting.
- Added analysis-only workflows for existing JSON, CSV, and XLSX evidence.
