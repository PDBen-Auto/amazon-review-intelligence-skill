#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from datetime import datetime


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
    return "content:" + "|".join([
        normalize(review.get("Title")),
        normalize(review.get("Text")),
        normalize(review.get("OriginDescription")),
        normalize(review.get("OverallRating")),
        normalize(review.get("Author")),
    ])


def fetch_text(url, timeout, retries):
    last_error = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                final_host = (urllib.parse.urlparse(response.geturl()).hostname or "").lower()
                if not (final_host == "woot.com" or final_host.endswith(".woot.com")):
                    raise ValueError(f"Woot request redirected outside woot.com: {final_host}")
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if 400 <= exc.code < 500 and exc.code != 429:
                raise
            last_error = exc
        except Exception as exc:
            last_error = exc
        if attempt < retries:
            time.sleep(min(2 ** attempt, 4))
    raise last_error


def resolve_woot_offer(asin, offer_url, timeout, retries):
    parsed = urllib.parse.urlparse(offer_url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not (host == "woot.com" or host.endswith(".woot.com")) or parsed.username or parsed.password:
        raise ValueError("Woot offer URL must use HTTPS on a woot.com host")
    if not parsed.path.startswith("/offers/"):
        raise ValueError("Provide a Woot /offers/ product URL, not a search or review URL")
    page = fetch_text(offer_url, timeout, retries)
    items_match = re.search(r"\bofferItems\s*=\s*", page)
    offer_match = re.search(r'\bofferId\s*=\s*"([0-9a-fA-F-]{36})"', page)
    if not items_match or not offer_match:
        raise ValueError("Woot offer page does not expose offerItems and offerId")
    items, _ = json.JSONDecoder().raw_decode(page[items_match.end():].lstrip())
    if not isinstance(items, list):
        raise ValueError("Woot offerItems is not a list")
    matching = [item for item in items if str(item.get("Asin") or "").upper() == asin]
    if not matching:
        shown = sorted({str(item.get("Asin")) for item in items if item.get("Asin")})
        raise ValueError(f"ASIN mismatch: requested {asin}; Woot offer contains {shown}")
    review_base = f"https://{host}/review/Reviews/{asin}"
    return {"offer_url": offer_url, "offer_id": offer_match.group(1), "item_id": matching[0].get("Id"), "review_base": review_base}


def fetch_reviews(source, filter_value=0, sort_value=0, delay=0.15, timeout=18, retries=2, max_pages=12, errors=None):
    reviews = []
    paging_next = None
    seen_cursors = set()
    for page_number in range(1, max_pages + 1):
        params = {
            "offerid": source["offer_id"],
            "filter": str(filter_value),
            "isVerified": "false",
            "sort": str(sort_value),
        }
        if paging_next:
            params["pagingNext"] = paging_next
        else:
            params["page"] = "1"
        url = source["review_base"] + "?" + urllib.parse.urlencode(params)
        try:
            data = json.loads(fetch_text(url, timeout=timeout, retries=retries))
            if not isinstance(data, dict) or not isinstance(data.get("Reviews"), list):
                raise ValueError("Unexpected Woot review response")
        except (ValueError, OSError) as exc:
            if errors is None:
                raise
            errors.append({"filter": filter_value, "sort": sort_value, "page": page_number, "error": str(exc)})
            break
        batch = data.get("Reviews") or []
        if not batch:
            break
        reviews.extend(batch)
        paging_next = data.get("PagingNext") or ""
        if not paging_next:
            break
        if paging_next in seen_cursors:
            if errors is None:
                raise ValueError(f"Repeated Woot paging cursor for filter={filter_value} sort={sort_value}")
            errors.append({"filter": filter_value, "sort": sort_value, "page": page_number, "error": "Repeated paging cursor"})
            break
        seen_cursors.add(paging_next)
        time.sleep(max(delay, 0))
    else:
        print(f"Pagination cap reached for filter={filter_value} sort={sort_value}; coverage remains unknown", file=sys.stderr)
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


def scrape(source, mode, delay, timeout, retries):
    seen = set()
    unique = []
    errors = []
    if mode == "basic":
        rows = fetch_reviews(source, 0, 0, delay, timeout, retries, errors=errors)
        add_unique(unique, seen, rows)
        print(f"basic: fetched={len(rows)} unique={len(unique)}", file=sys.stderr)
        return unique, errors

    sorts = [0] if mode == "full" else [0, 1]
    for star in [5, 4, 3, 2, 1]:
        before = len(unique)
        for sort_value in sorts:
            rows = fetch_reviews(source, star, sort_value, delay, timeout, retries, errors=errors)
            added = add_unique(unique, seen, rows)
            if rows:
                print(f"star={star} sort={sort_value}: fetched={len(rows)} new={added}", file=sys.stderr)
        print(f"star={star} subtotal={len(unique) - before}", file=sys.stderr)
    return unique, errors


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
    parser.add_argument("--mode", choices=["basic", "full", "max"], default="full")
    parser.add_argument("--woot-offer-url", required=True, help="Exact Woot product /offers/ URL containing the requested ASIN")
    parser.add_argument("--output", "-o")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--timeout", type=int, default=18)
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()

    asin = args.asin.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{10}", asin):
        parser.error(f"Invalid ASIN: {args.asin}")
    try:
        source = resolve_woot_offer(asin, args.woot_offer_url, args.timeout, args.retries)
        print(f"Collecting {asin} from {source['review_base']} in {args.mode} mode", file=sys.stderr)
        reviews, errors = scrape(source, args.mode, args.delay, args.timeout, args.retries)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Collection failed for {asin}: {exc}", file=sys.stderr)
        return 2
    summary = build_summary(asin, reviews, args.mode)
    summary["status"] = "partial" if errors else ("collected" if reviews else "empty_unverified")
    summary["coverage"] = "unknown"
    summary["collection_errors"] = errors
    summary["source"] = source
    result = summary if args.summary else {"summary": summary, "reviews": reviews}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)
    print(json.dumps(summary, ensure_ascii=False), file=sys.stderr)
    return 4 if errors else (0 if reviews else 3)


if __name__ == "__main__":
    sys.exit(main())
