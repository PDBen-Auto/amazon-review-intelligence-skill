#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime


BASE_URL = "https://www.woot.com/review/Reviews/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}


def normalize(value):
    value = html.unescape(str(value or "")).lower()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", value)


def review_key(review):
    review_id = review.get("ReviewId") or review.get("Id") or review.get("id")
    if review_id:
        return "id:" + str(review_id)
    date_or_author = normalize(review.get("OriginDescription")) or normalize(review.get("Author"))
    return "content:" + "|".join([
        normalize(review.get("Title")),
        normalize(str(review.get("Text") or "")[:120]),
        date_or_author,
    ])


def fetch_page(url, timeout, retries):
    last_error = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2 ** attempt, 4))
    raise last_error


def fetch_reviews(asin, filter_value=0, sort_value=0, delay=0.15, timeout=18, retries=2, max_pages=12):
    reviews = []
    paging_next = None
    for page_number in range(1, max_pages + 1):
        params = {
            "filter": str(filter_value),
            "isVerified": "false",
            "sort": str(sort_value),
        }
        if paging_next:
            params["pagingNext"] = paging_next
        else:
            params["page"] = "1"
        url = BASE_URL + asin + "?" + urllib.parse.urlencode(params)
        try:
            data = fetch_page(url, timeout=timeout, retries=retries)
        except Exception as exc:
            print(f"Error filter={filter_value} sort={sort_value} page={page_number}: {exc}", file=sys.stderr)
            break
        batch = data.get("Reviews") or []
        if not batch:
            break
        reviews.extend(batch)
        paging_next = data.get("PagingNext") or ""
        if not paging_next:
            break
        time.sleep(max(delay, 0))
    return reviews


def add_unique(target, seen, reviews):
    added = 0
    for review in reviews:
        key = review_key(review)
        if key not in seen:
            seen.add(key)
            target.append(review)
            added += 1
    return added


def scrape(asin, mode, delay, timeout, retries):
    seen = set()
    unique = []
    if mode == "basic":
        rows = fetch_reviews(asin, 0, 0, delay, timeout, retries)
        add_unique(unique, seen, rows)
        print(f"basic: fetched={len(rows)} unique={len(unique)}", file=sys.stderr)
        return unique

    sorts = [0] if mode == "full" else [0, 1, 2, 3]
    for star in [5, 4, 3, 2, 1]:
        before = len(unique)
        for sort_value in sorts:
            rows = fetch_reviews(asin, star, sort_value, delay, timeout, retries)
            added = add_unique(unique, seen, rows)
            if rows:
                print(f"star={star} sort={sort_value}: fetched={len(rows)} new={added}", file=sys.stderr)
        print(f"star={star} subtotal={len(unique) - before}", file=sys.stderr)
    return unique


def parse_review_date(review):
    description = str(review.get("OriginDescription") or "")
    match = re.search(r"on (\w+ \d{1,2},?\s+\d{4})", description)
    if match:
        value = re.sub(r"\s+", " ", match.group(1).replace(",", "").strip())
        try:
            return datetime.strptime(value, "%B %d %Y")
        except ValueError:
            pass
    match = re.search(r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})", description)
    if match:
        try:
            return datetime.strptime(f"{match.group(1)} {match.group(2)} {match.group(3)}", "%B %d %Y")
        except ValueError:
            pass
    return None


def build_summary(asin, reviews, mode):
    stars = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    verified = 0
    with_images = 0
    with_video = 0
    monthly = {}
    dates = []
    for review in reviews:
        rating = int(review.get("OverallRating") or 0)
        if rating in stars:
            stars[rating] += 1
        verified += bool(review.get("IsVerifiedPurchase"))
        with_images += bool(review.get("ImageUrls"))
        with_video += bool(review.get("MediaUrls"))
        date = parse_review_date(review)
        if date:
            dates.append(date)
            key = date.strftime("%Y-%m")
            monthly.setdefault(key, {"count": 0, "rating_total": 0})
            monthly[key]["count"] += 1
            monthly[key]["rating_total"] += rating
    distribution = [
        {"month": key, "count": value["count"], "avg_rating": round(value["rating_total"] / value["count"], 1)}
        for key, value in sorted(monthly.items(), reverse=True)
    ]
    return {
        "asin": asin,
        "mode": mode,
        "total_reviews": len(reviews),
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "star_distribution": stars,
        "verified_purchases": verified,
        "with_images": with_images,
        "with_video": with_video,
        "monthly_distribution": distribution,
        "date_range": {"earliest": min(dates).strftime("%Y-%m-%d"), "latest": max(dates).strftime("%Y-%m-%d")} if dates else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Collect Amazon US written reviews from a public review endpoint")
    parser.add_argument("asin")
    parser.add_argument("--mode", choices=["basic", "full", "max"], default="max")
    parser.add_argument("--output", "-o")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--timeout", type=int, default=18)
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()

    asin = args.asin.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{10}", asin):
        parser.error(f"Invalid ASIN: {args.asin}")
    print(f"Collecting {asin} in {args.mode} mode", file=sys.stderr)
    reviews = scrape(asin, args.mode, args.delay, args.timeout, args.retries)
    summary = build_summary(asin, reviews, args.mode)
    result = summary if args.summary else {"summary": summary, "reviews": reviews}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)
    print(json.dumps(summary, ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
