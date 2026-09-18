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


def read_count(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return len(data.get("reviews") or [])
    except Exception:
        return 0


def write_status(path: Path, rows: list[dict]) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch Amazon US written-review collection with checkpointing")
    parser.add_argument("asins", nargs="+", help="One or more 10-character ASINs")
    parser.add_argument("--output-dir", required=True, help="Batch output directory")
    parser.add_argument("--mode", choices=["basic", "full", "max"], default="max")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between ASINs")
    parser.add_argument("--resume", action="store_true", help="Keep valid existing captures")
    args = parser.parse_args()

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
        log_path = asin_dir / "collector.log"

        if args.resume and target.exists():
            count = read_count(target)
            if count > 0:
                rows.append({"ASIN": asin, "status": "existing", "reviews": count, "updatedAt": datetime.now().isoformat()})
                write_status(status_path, rows)
                continue

        row = {"ASIN": asin, "status": "running", "reviews": 0, "updatedAt": datetime.now().isoformat()}
        rows.append(row)
        write_status(status_path, rows)
        command = [sys.executable, str(scraper), asin, "--mode", args.mode, "-o", str(target)]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
        log_path.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")
        count = read_count(target)
        row.update({
            "status": ("done" if count > 0 else "needs_browser_fallback") if result.returncode == 0 else f"error:{result.returncode}",
            "reviews": count,
            "updatedAt": datetime.now().isoformat(),
        })
        write_status(status_path, rows)
        time.sleep(max(args.delay, 0))

    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
