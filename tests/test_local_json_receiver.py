import importlib.util
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "local_json_receiver.py"
SPEC = importlib.util.spec_from_file_location("local_json_receiver", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def post(url, payload, token="test-token", origin="https://www.amazon.com"):
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Origin": origin,
            "X-Review-Receiver-Token": token,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir).resolve()
        server = MODULE.make_server("127.0.0.1", 0, root, "test-token", max_bytes=1024)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{server.server_port}"
        try:
            payload = {
                "asin": "SYNTHETIC1",
                "name": "demo.json",
                "data": {"reviews": [{"text": "Synthetic review"}]},
            }
            status, result = post(url, payload)
            assert status == 200
            assert result["path"] == "SYNTHETIC1/demo.json"
            assert str(root) not in json.dumps(result)
            assert (root / result["path"]).exists()

            status, result = post(url, payload)
            assert status == 200
            assert result["path"] == "SYNTHETIC1/demo-2.json"

            status, _ = post(url, payload, token="wrong-token")
            assert status == 401

            status, _ = post(url, payload, origin="https://example.com")
            assert status == 403

            status, _ = post(url, {"data": "x" * 2000})
            assert status == 413
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    try:
        MODULE.make_server("0.0.0.0", 0, Path.cwd(), "test-token")
    except ValueError:
        pass
    else:
        raise AssertionError("Non-loopback binding must be rejected")
    print("local_json_receiver security controls: OK")


if __name__ == "__main__":
    main()
