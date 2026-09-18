#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys
from datetime import datetime


def normalize(value):
    value = html.unescape(str(value or "")).lower().strip()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", value)


def dedup_key(review):
    review_id = review.get("review_id") or review.get("id")
    if review_id:
        return "id:" + str(review_id)
    title = normalize(review.get("title"))
    body = normalize(str(review.get("text") or ""))
    date = normalize(review.get("date") or review.get("date_text"))
    rating = normalize(review.get("rating"))
    author = normalize(review.get("author"))
    return "content:" + "|".join([title, body, date, rating, author])


def media_list(raw):
    if not raw:
        return []
    if isinstance(raw, str):
        return [line.strip() for line in raw.splitlines() if line.strip()]
    result = []
    for item in raw:
        if isinstance(item, str):
            url = item
        elif isinstance(item, dict):
            url = item.get("src") or item.get("url") or item.get("href") or item.get("poster") or ""
        else:
            url = ""
        if url and url not in result:
            result.append(url)
    return result


def parse_date(value):
    value = str(value or "")
    match = re.search(r"on (\w+ \d{1,2}, \d{4})", value)
    if match:
        value = match.group(1)
        fmt = "%B %d, %Y"
    else:
        fmt = "%Y%m%d" if re.fullmatch(r"\d{8}", value) else "%Y-%m-%d"
    try:
        return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
    except ValueError:
        return None


def interface_review(raw):
    return {
        "review_id": value(raw, "ReviewId", "Id", "id", "review_id"),
        "title": html.unescape(str(value(raw, "Title", "title") or "")),
        "text": value(raw, "Text", "text", "body") or "",
        "rating": value(raw, "OverallRating", "rating", "stars") or 0,
        "date": parse_date(value(raw, "OriginDescription", "date", "date_text")),
        "date_text": value(raw, "OriginDescription", "date_text", "date") or "",
        "author": value(raw, "Author", "author", "评论人"),
        "variant": value(raw, "variant", "variation", "评论产品的属性"),
        "verified_purchase": value(raw, "IsVerifiedPurchase", "verified_purchase", "verified", "是否认证购买"),
        "vine_review": value(raw, "IsVineReview", "vine_review", "Vine"),
        "helpful_votes": value(raw, "HelpfulVotes", "helpful_votes", "helpful", "Helpful"),
        "image_urls": media_list(value(raw, "ImageUrls", "image_urls", "图片URL")),
        "media_urls": media_list(value(raw, "MediaUrls", "media_urls", "视频URL")),
        "source": "interface",
    }


def value(raw, *names):
    for name in names:
        if raw.get(name) not in (None, ""):
            return raw[name]
    return None


def connector_review(raw):
    rating = value(raw, "评星", "rating", "stars") or 0
    try:
        rating = int(float(rating))
    except (TypeError, ValueError):
        rating = 0
    return {
        "review_id": value(raw, "评论ID", "review_id", "id"),
        "title": value(raw, "标题", "title") or "", "text": value(raw, "评论", "评论内容", "text", "body") or "",
        "rating": rating, "date": parse_date(value(raw, "评论日期", "date")),
        "date_text": value(raw, "评论日期", "date") or "", "author": value(raw, "评论人", "author"),
        "variant": value(raw, "评论产品的属性", "variant", "variation"),
        "verified_purchase": value(raw, "是否认证购买", "verified_purchase"), "vine_review": value(raw, "Vine", "vine_review"),
        "helpful_votes": value(raw, "Helpful", "helpful_votes"),
        "image_urls": media_list(value(raw, "图片URL", "image_urls")),
        "media_urls": media_list(value(raw, "视频URL", "media_urls")), "source": "connector",
    }


def load_reviews(path):
    with open(path, encoding="utf-8-sig") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else data.get("reviews") or data.get("Reviews") or []


def merge_missing(existing, incoming):
    for field in ["review_id", "title", "text", "rating", "date", "date_text", "author", "variant", "verified_purchase", "vine_review", "helpful_votes"]:
        if existing.get(field) in (None, "", 0) and incoming.get(field) not in (None, "", 0):
            existing[field] = incoming[field]
    for field in ["image_urls", "media_urls"]:
        existing[field] = list(dict.fromkeys((existing.get(field) or []) + (incoming.get(field) or [])))
    if existing["source"] != incoming["source"]:
        existing["source"] = "merged"


def merge_reviews(interface_file=None, connector_file=None):
    merged, seen = [], {}
    interface_keys, connector_keys = set(), set()
    stats = {"interface_total": 0, "connector_total": 0, "overlap": 0}
    if interface_file:
        rows = load_reviews(interface_file)
        stats["interface_total"] = len(rows)
        for raw in rows:
            review = interface_review(raw)
            key = dedup_key(review)
            interface_keys.add(key)
            if key in seen:
                merge_missing(seen[key], review)
            else:
                seen[key] = review
                merged.append(review)
    if connector_file:
        rows = load_reviews(connector_file)
        stats["connector_total"] = len(rows)
        for raw in rows:
            review = connector_review(raw)
            key = dedup_key(review)
            connector_keys.add(key)
            if key in seen:
                merge_missing(seen[key], review)
            else:
                seen[key] = review
                merged.append(review)
    merged.sort(key=lambda row: row.get("date") or "0000-00-00", reverse=True)
    overlap = interface_keys & connector_keys
    stats.update({
        "interface_unique": len(interface_keys), "connector_unique": len(connector_keys),
        "overlap": len(overlap), "merged_total": len(merged),
        "interface_only": len(interface_keys - connector_keys),
        "connector_only": len(connector_keys - interface_keys),
    })
    return merged, stats


def main():
    parser = argparse.ArgumentParser(description="Deduplicate and merge Amazon review JSON sources")
    parser.add_argument("--woot", dest="interface", help="Interface JSON file")
    parser.add_argument("--sorftime", "--sf", dest="connector", help="Connector JSON file")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    if not args.interface and not args.connector:
        parser.error("At least one source is required")
    reviews, stats = merge_reviews(args.interface, args.connector)
    output = json.dumps({"stats": stats, "reviews": reviews}, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)
    print(json.dumps(stats, ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
