#!/usr/bin/env python3
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Receive browser review JSON on localhost")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    root = Path(args.output_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    class Handler(BaseHTTPRequestHandler):
        def cors(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

        def do_OPTIONS(self):
            self.send_response(204)
            self.cors()
            self.end_headers()

        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            try:
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                asin = re.sub(r"[^A-Z0-9]", "", str(payload.get("asin", "UNKNOWN")).upper())[:20]
                name = re.sub(r"[^A-Za-z0-9_.-]", "_", str(payload.get("name", f"{asin}_browser_reviews.json")))
                target_dir = root / asin
                target_dir.mkdir(parents=True, exist_ok=True)
                target = target_dir / name
                target.write_text(json.dumps(payload.get("data", payload), ensure_ascii=False, indent=2), encoding="utf-8")
                body = json.dumps({"ok": True, "path": str(target)}, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
            except Exception as exc:
                body = json.dumps({"ok": False, "error": str(exc)}).encode("utf-8")
                self.send_response(500)
            self.cors()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            return

    print(f"Listening on http://{args.host}:{args.port} -> {root}")
    HTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
