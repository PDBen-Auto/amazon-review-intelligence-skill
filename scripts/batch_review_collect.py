#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")


def read_count(path: Path, offer_url: str | None = None) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        summary = data.get("summary", {})
        if summary.get("status") != "collected" or (offer_url and summary.get("source", {}).get("offer_url") != offer_url):
            return 0
        return len(data.get("reviews") or [])
    except Exception:
        return 0


def read_partial_count(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return len(data.get("reviews") or []) if data.get("summary", {}).get("status") == "partial" else 0
    except Exception:
        return 0


def write_status(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch Amazon US written-review collection with checkpointing")
    parser.add_argument("asins", nargs="+", help="One or more 10-character ASINs")
    parser.add_argument("--output-dir", required=True, help="Batch output directory")
    parser.add_argument("--mode", choices=["basic", "full", "max"], default="full")
    parser.add_argument("--woot-offer-map", help="JSON object mapping each ASIN to its verified Woot /offers/ URL")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between ASINs")
    parser.add_argument("--resume", action="store_true", help="Keep valid existing captures")
    args = parser.parse_args()
    offer_map = {}
    if args.woot_offer_map:
        offer_map = json.loads(Path(args.woot_offer_map).read_text(encoding="utf-8-sig"))
        if not isinstance(offer_map, dict):
            parser.error("--woot-offer-map must contain a JSON object")
        offer_map = {str(key).upper(): value for key, value in offer_map.items()}

    asins = []
    for value in args.asins:
        asin = value.strip().upper()
        if not ASIN_RE.fullmatch(asin):
            parser.error(f"Invalid ASIN: {value}")
        if asin not in asins:
            asins.append(asin)

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    status_path = output_dir / "collection_status.json"
    scraper = Path(__file__).with_name("amazon_review_scraper.py")
    rows = []

    for asin in asins:
        asin_dir = output_dir / asin
        asin_dir.mkdir(parents=True, exist_ok=True)
        target = asin_dir / f"{asin}_woot_{args.mode}.json"
        pending = asin_dir / f"{asin}_woot_{args.mode}.pending.json"
        log_path = asin_dir / "collector.log"
        offer_url = offer_map.get(asin)

        if not isinstance(offer_url, str) or not offer_url:
            rows.append({"ASIN": asin, "status": "woot_mapping_missing", "reviews": 0,
                         "previousCaptureRetained": target.exists(), "updatedAt": datetime.now().isoformat()})
            write_status(status_path, rows)
            continue

        if args.resume and target.exists():
            count = read_count(target, offer_url)
            if count > 0:
                rows.append({"ASIN": asin, "status": "existing", "reviews": count, "updatedAt": datetime.now().isoformat()})
                write_status(status_path, rows)
                continue

        row = {"ASIN": asin, "status": "running", "reviews": 0, "updatedAt": datetime.now().isoformat()}
        rows.append(row)
        write_status(status_path, rows)
        command = [sys.executable, str(scraper), asin, "--mode", args.mode, "--woot-offer-url", offer_url, "-o", str(pending)]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
        log_path.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
        count = read_count(pending)
        partial_count = read_partial_count(pending) if result.returncode == 4 else 0
        if result.returncode == 0 and count > 0:
            pending.replace(target)
        row.update({
            "status": "done" if result.returncode == 0 and count > 0 else ("empty_unverified" if result.returncode == 3 else ("woot_partial" if partial_count else "woot_failed")),
            "reviews": count or partial_count,
            "exitCode": result.returncode,
            "previousCaptureRetained": target.exists() if result.returncode != 0 else False,
            "error": result.stderr.strip().splitlines()[-1] if result.returncode != 0 and result.stderr.strip() else None,
            "updatedAt": datetime.now().isoformat(),
        })
        write_status(status_path, rows)
        time.sleep(max(args.delay, 0))

    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
