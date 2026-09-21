#!/usr/bin/env python3
import argparse
import hmac
import ipaddress
import json
import os
import re
import secrets
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit


DEFAULT_MAX_BYTES = 8 * 1024 * 1024
AMAZON_ORIGIN_HOSTS = {
    "amazon.ae",
    "amazon.ca",
    "amazon.cn",
    "amazon.co.jp",
    "amazon.co.uk",
    "amazon.com",
    "amazon.com.au",
    "amazon.com.be",
    "amazon.com.br",
    "amazon.com.mx",
    "amazon.com.tr",
    "amazon.de",
    "amazon.eg",
    "amazon.es",
    "amazon.fr",
    "amazon.in",
    "amazon.it",
    "amazon.nl",
    "amazon.pl",
    "amazon.sa",
    "amazon.se",
    "amazon.sg",
}


def is_loopback_host(host: str) -> bool:
    if host.lower() == "localhost":
        return True
    try:
        return all(
            ipaddress.ip_address(item[4][0]).is_loopback
            for item in socket.getaddrinfo(host, None)
        )
    except (socket.gaierror, ValueError):
        return False


def is_allowed_origin(origin: str | None, extra_origins: set[str]) -> bool:
    if not origin:
        return True
    if origin in extra_origins:
        return True
    parsed = urlsplit(origin)
    if parsed.scheme != "https" or not parsed.hostname:
        return False
    hostname = parsed.hostname.lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname in AMAZON_ORIGIN_HOSTS


def clean_component(value: object, fallback: str, max_length: int) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "_", str(value or fallback)).strip("._")
    return (cleaned or fallback)[:max_length]


def safe_target_dir(root: Path, asin: str) -> Path:
    target_dir = root / asin
    if target_dir.exists() and (target_dir.is_symlink() or not target_dir.is_dir()):
        raise ValueError("Target ASIN path is not a normal directory")
    target_dir.mkdir(mode=0o700, parents=False, exist_ok=True)
    resolved = target_dir.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Target path escapes the configured output directory")
    return resolved


def write_unique_json(target_dir: Path, name: str, payload: object) -> Path:
    requested = Path(name)
    stem = requested.stem or "browser_reviews"
    suffix = requested.suffix or ".json"
    if suffix.lower() != ".json":
        suffix = f"{suffix}.json"
    encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    for number in range(1, 1001):
        candidate_name = f"{stem}{suffix}" if number == 1 else f"{stem}-{number}{suffix}"
        candidate = target_dir / candidate_name
        try:
            descriptor = os.open(candidate, flags, 0o600)
        except FileExistsError:
            continue
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
        return candidate
    raise FileExistsError("Could not allocate a unique JSON filename")


def build_handler(root: Path, token: str, max_bytes: int, extra_origins: set[str]):
    class Handler(BaseHTTPRequestHandler):
        def send_cors(self, origin: str | None) -> None:
            if origin and is_allowed_origin(origin, extra_origins):
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
            self.send_header(
                "Access-Control-Allow-Headers",
                "Authorization, Content-Type, X-Review-Receiver-Token",
            )
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

        def send_json(self, status: int, payload: dict, origin: str | None = None) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_cors(origin)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def authorized(self) -> bool:
            provided = self.headers.get("X-Review-Receiver-Token", "")
            bearer = self.headers.get("Authorization", "")
            if bearer.startswith("Bearer "):
                provided = bearer[7:]
            return bool(provided) and hmac.compare_digest(provided, token)

        def do_OPTIONS(self) -> None:
            origin = self.headers.get("Origin")
            if not is_allowed_origin(origin, extra_origins):
                self.send_json(403, {"ok": False, "error": "Origin is not allowed"})
                return
            self.send_response(204)
            self.send_cors(origin)
            self.end_headers()

        def do_POST(self) -> None:
            origin = self.headers.get("Origin")
            if not is_allowed_origin(origin, extra_origins):
                self.send_json(403, {"ok": False, "error": "Origin is not allowed"})
                return
            if not self.authorized():
                self.send_json(401, {"ok": False, "error": "Missing or invalid receiver token"}, origin)
                return

            raw_length = self.headers.get("Content-Length")
            try:
                length = int(raw_length or "")
            except ValueError:
                self.send_json(411, {"ok": False, "error": "A valid Content-Length is required"}, origin)
                return
            if length <= 0:
                self.send_json(400, {"ok": False, "error": "Request body is empty"}, origin)
                return
            if length > max_bytes:
                self.send_json(413, {"ok": False, "error": "Request body exceeds the configured limit"}, origin)
                return

            try:
                raw = self.rfile.read(length)
                if len(raw) != length:
                    raise ValueError("Request body ended before Content-Length")
                payload = json.loads(raw.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("Top-level JSON value must be an object")
                asin = clean_component(payload.get("asin"), "UNKNOWN", 20).upper()
                default_name = f"{asin}_browser_reviews.json"
                name = clean_component(payload.get("name"), default_name, 120)
                target_dir = safe_target_dir(root, asin)
                target = write_unique_json(target_dir, name, payload.get("data", payload))
                relative_path = target.relative_to(root).as_posix()
                self.send_json(200, {"ok": True, "path": relative_path}, origin)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                self.send_json(400, {"ok": False, "error": str(exc)}, origin)
            except Exception as exc:
                self.send_json(500, {"ok": False, "error": type(exc).__name__}, origin)

        def log_message(self, fmt, *args):
            return

    return Handler


def make_server(
    host: str,
    port: int,
    root: Path,
    token: str,
    max_bytes: int = DEFAULT_MAX_BYTES,
    extra_origins: set[str] | None = None,
) -> HTTPServer:
    if not is_loopback_host(host):
        raise ValueError("The receiver can bind only to a loopback host")
    handler = build_handler(root.resolve(), token, max_bytes, extra_origins or set())
    return HTTPServer((host, port), handler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Receive browser review JSON on localhost")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token", help="Receiver token; generated when omitted")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument(
        "--allow-origin",
        action="append",
        default=[],
        help="Additional exact HTTPS origin allowed to POST; may be repeated",
    )
    args = parser.parse_args()
    if args.max_bytes < 1024 or args.max_bytes > 64 * 1024 * 1024:
        parser.error("--max-bytes must be between 1 KiB and 64 MiB")

    root = Path(args.output_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    token = args.token or secrets.token_urlsafe(32)
    server = make_server(args.host, args.port, root, token, args.max_bytes, set(args.allow_origin))
    print(f"Listening on http://{args.host}:{server.server_port} -> {root}")
    print("Send the token as X-Review-Receiver-Token or Authorization: Bearer <token>.")
    print(f"Receiver token: {token}")
    server.serve_forever()


if __name__ == "__main__":
    main()
