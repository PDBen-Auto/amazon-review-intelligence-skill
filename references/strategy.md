# Collection Strategy

## Decision table

| Situation | Primary action | Fallback | Stop/label |
|---|---|---|---|
| US ASIN with an exact Woot offer match | Verify offer ASIN/ID, probe `basic`, then requested mode | Amazon browser review pages or authorized connector | Label as written-review coverage, not all ratings |
| US ASIN without a Woot offer match | Record `woot_mapping_missing` | Amazon browser review pages or authorized connector | Do not infer that the ASIN has no Amazon reviews |
| Non-US marketplace | Multi-market connector | Browser on the requested marketplace | Never use the US-only interface as if it were cross-market |
| Interface returns zero | Check Amazon product/review page | Capture browser reviews | Zero is not proof of no reviews |
| Interface returns fewer than the visible written-review signal | Add browser recent/top pages and deduplicate | Report residual limit | Do not replace a larger interface set with a smaller browser set |
| Woot API returns 404, malformed JSON, or unsupported schema | Record `woot_failed`, then use browser/manual capture | Ask user to open page when navigation fails | Preserve logs; never record zero as successful collection |
| Robot Check/CAPTCHA/sign-in/account warning | Stop browser automation | Ask user for the narrow next action | Never bypass or accelerate requests |

## Coverage rules

- Amazon's displayed rating count includes star-only ratings. Compare collected rows with written-review signals, not the rating total.
- Interface `max` mode explores star and sort combinations. It can exceed the browser's normal 100-review page limit, but high-volume five-star reviews may still be capped.
- For broader collection, use the five star groups in Top order first. Check the deduplicated gain over `basic`, then run Most Recent only when recency matters or more coverage is required. Measure the new unique reviews from each sort; do not add raw combination counts. A timeout after successful pages is `partial`, with the failed filter/page recorded and prior valid capture retained.
- Browser review pages commonly expose up to 10 pages. Some pages return duplicate page 1 content for page 2; stop after a repeated review-ID set.
- On Woot, `Show more reviews` loads another batch through `PagingNext`; keep requesting while the cursor advances. The separate `read more` control expands a long review body. Confirm interface `Text` is complete, or expand the browser body before capture.
- Never claim 100% coverage unless the written-review population is known and the unique collected count matches it.

## Batch pacing

- Run Woot ASINs sequentially with a 1-2 second gap after exact offer matching.
- Run browser ASINs sequentially with a 3-7 second gap and no parallel page storms.
- Checkpoint after every ASIN and after every browser page.
- Resume from valid existing JSON rather than recollecting completed ASINs.

## Merge priority

Prefer records in this order:

1. Interface record with author, verified purchase, Vine, helpful votes, and media.
2. Browser record with stable review ID and current visible text/media.
3. Connector record with variant attributes.

Merge fields rather than concatenating duplicate records.

## Strategy examples

### Interface succeeds

Keep the interface set as the base. Use browser pages only when the user asked for recent visible reviews, product-page fields, or a coverage check.

### Interface returns zero but page has reviews

Capture recent pages through the browser, stopping on empty/repeated content. Mark the source as browser fallback and retain the zero-interface log.

### Browser cannot navigate but the user can

Ask the user to open the exact URL in the in-app browser. Claim the already-open tab and read it without reloading. This is the preferred manual handoff.

### Partial batch

Deliver successful ASINs and clearly list remaining statuses only after safe retries and manual-page options are exhausted.
