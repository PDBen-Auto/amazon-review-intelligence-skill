# Browser Fallback

## Safety boundary

- Read only visible product and review content.
- Do not read cookies, local storage, profiles, passwords, browsing history, account pages, addresses, or orders.
- Do not click Helpful, Report, purchase, write-review, account, or preference controls.
- Stop on CAPTCHA, Robot Check, sign-in wall, account warning, or unexpected redirect.
- Ask before solving a CAPTCHA. Never bypass it.

## Preferred page

Use:

```text
https://www.amazon.com/product-reviews/{ASIN}/?reviewerType=all_reviews&sortBy=recent&pageNumber=1
```

Use the marketplace domain that matches the request.

## Capture sequence

1. Verify the URL contains the expected ASIN.
2. Check the page for Robot Check, CAPTCHA, sign-in wall, and account warnings.
3. Identify review cards with `[data-hook="review"]`.
4. Expand `[data-hook="show-more-button"]` only to reveal clipped text.
5. Extract the current page in one bounded DOM evaluation.
6. Navigate page numbers sequentially, normally 1 through 10.
7. Deduplicate by review ID or normalized content after every page.
8. Stop on no cards, zero new unique reviews, repeated ID set, disabled next page, or a safety boundary.
9. Save a checkpoint JSON after each page.

## Review fields

Extract:

| Field | Preferred selector/source |
|---|---|
| ID | review card `id` or `data-review-id` |
| Author | `.a-profile-name` |
| Rating | `[data-hook="review-star-rating"]`, `[data-hook="cmps-review-star-rating"]` |
| Title | `[data-hook="review-title"]` |
| Date | `[data-hook="review-date"]` |
| Verified | `[data-hook="avp-badge"]` |
| Body | `[data-hook="review-body"]` |
| Helpful | `[data-hook="helpful-vote-statement"]` |
| Images | media images inside the review card; exclude avatars/sprites |
| Video | `video`, `source`, and review-media links inside the card |

## Browser JSON schema

```json
{
  "asin": "B0XXXXXXXX",
  "capturedAt": "ISO-8601",
  "reviewCount": 10,
  "reviews": [
    {
      "id": "R...",
      "profile": "Reviewer",
      "rating": "5.0 out of 5 stars",
      "title": "Full title",
      "date": "Reviewed ...",
      "verified": "Verified Purchase",
      "body": "Full review text",
      "helpful": "2 people found this helpful",
      "mediaImages": ["https://..."],
      "videoElements": ["https://..."],
      "pageUrl": "https://...",
      "pageNumber": 1
    }
  ],
  "captureLog": [],
  "stopped": "No reviews on page 4"
}
```

## Manual handoff

If automated navigation repeatedly times out:

1. Ask the user to open the exact product or review URL in the in-app browser.
2. Wait until they confirm the page is visibly loaded.
3. Claim the existing tab by URL and title.
4. Extract without calling `goto` or `reload`.
5. Leave the user's tab open after releasing control.
