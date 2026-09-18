# Collection Strategy

## Decision table

| Situation | Primary action | Fallback | Stop/label |
|---|---|---|---|
| US ASIN, maximum requested | Interface `max` mode | Browser review pages | Label as written-review coverage, not all ratings |
| US ASIN, quick preview | Interface `basic` mode | One browser page if zero | Do not expand scope silently |
| Non-US marketplace | Multi-market connector | Browser on the requested marketplace | Never use the US-only interface as if it were cross-market |
| Interface returns zero | Check Amazon product/review page | Capture browser reviews | Zero is not proof of no reviews |
| Interface returns fewer than the visible written-review signal | Add browser recent/top pages and deduplicate | Report residual limit | Do not replace a larger interface set with a smaller browser set |
| API unavailable or blocked | Use browser/manual capture | Ask user to open page when navigation fails | Preserve partial results and logs |
| Robot Check/CAPTCHA/sign-in/account warning | Stop browser automation | Ask user for the narrow next action | Never bypass or accelerate requests |

## Coverage rules

- Amazon's displayed rating count includes star-only ratings. Compare collected rows with written-review signals, not the rating total.
- Interface `max` mode explores star and sort combinations. It can exceed the browser's normal 100-review page limit, but high-volume five-star reviews may still be capped.
- Browser review pages commonly expose up to 10 pages. Some pages return duplicate page 1 content for page 2; stop after a repeated review-ID set.
- A visible `See more` control usually expands review text. It is not evidence that a new page of reviews loaded.
- Never claim 100% coverage unless the written-review population is known and the unique collected count matches it.

## Batch pacing

- Run interface ASINs sequentially with a 1-2 second gap.
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
