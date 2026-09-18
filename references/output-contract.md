# Output Contract

## Folder layout

```text
batch-output/
  ASIN_reviews_ALL.xlsx
  reviews_summary.json
  collection_status.json
  B0XXXXXXXX/
    B0XXXXXXXX_woot_max.json
    B0XXXXXXXX_browser_reviews.json
    B0XXXXXXXX_reviews_raw.json
    B0XXXXXXXX_reviews.csv
    collector.log
    media/images/
```

One ASIN must map to one folder. Deduplicate repeated ASIN input before collection.

## Workbook sheets

### `all_reviews`

Use one review per row and retain full text.

Required columns:

```text
全局序号, ASIN, ASIN内序号, 评论ID, 评分, 标题, 评论内容, 评论人,
评论日期, 是否认证购买, Vine, Helpful, 图片数量,
图片1, 图片2, 图片3, 图片URL, 视频URL, 来源
```

Embed up to three downloaded images in `图片1` through `图片3`. Keep all image URLs in `图片URL` even when embedding fails.

### `reviews_summary`

Required columns:

```text
ASIN, 评论数, 5星, 4星, 3星, 2星, 1星, 有图评论, 有视频评论, 状态
```

### `product_comparison`

Include only when the user asks for product-page enrichment or horizontal comparison. Tailor feature columns to the product category; do not reuse cargo-carrier fields for mirrors or other unrelated products.

### `README`

Record ASIN count, written-review count, sheet descriptions, and limitations. Do not expose internal collection source names unless the user requested methodology details.

## Encoding and safety

- Write CSV as UTF-8 with BOM.
- Write JSON as UTF-8 with `ensure_ascii=false`.
- Use real Chinese headers, never mojibake or question marks.
- Prevent spreadsheet formula injection for untrusted review text beginning with `=`, `+`, `-`, or `@`.
- Keep video URLs as text. Do not download or execute media.

## Validation

Verify:

1. Workbook opens with `openpyxl`.
2. `all_reviews` row count equals the sum of `reviews_summary.评论数`.
3. Every requested ASIN appears in the summary.
4. No duplicate review IDs exist within an ASIN unless the ID is blank.
5. Headers contain no replacement characters or suspicious `?` runs.
6. Embedded-image count is reported separately from image-review count.
7. Product-page status is explicit when enrichment was requested.
