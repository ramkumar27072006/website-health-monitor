#!/usr/bin/env python3
"""Small, authorized website health monitor."""
from __future__ import annotations

import argparse
import json
import socket
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

SECURITY_HEADERS = (
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "Referrer-Policy",
)


def tls_days_left(url: str, timeout: float) -> int | None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return None
    host = parsed.hostname
    if not host:
        return None
    port = parsed.port or 443
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as raw:
        with context.wrap_socket(raw, server_hostname=host) as sock:
            expires = sock.getpeercert()["notAfter"]
    expiry = datetime.strptime(expires, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    return max(0, (expiry - datetime.now(timezone.utc)).days)


def check_url(url: str, timeout: float, slow_ms: int, tls_warning_days: int) -> dict:
    started = time.perf_counter()
    result = {"url": url, "checked_at": datetime.now(timezone.utc).isoformat(), "status": "FAIL"}
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True, headers={"User-Agent": "WebsiteHealthMonitor/1.0"})
        elapsed_ms = round((time.perf_counter() - started) * 1000)
        missing = [header for header in SECURITY_HEADERS if header not in response.headers]
        days = tls_days_left(response.url, timeout)
        warnings = []
        if elapsed_ms > slow_ms:
            warnings.append(f"slow response ({elapsed_ms}ms)")
        if response.url.startswith("https://") and missing:
            warnings.append("missing: " + ", ".join(missing))
        if days is not None and days <= tls_warning_days:
            warnings.append(f"TLS expires in {days} days")
        result.update({"status": "WARN" if warnings else "PASS", "http_status": response.status_code, "response_ms": elapsed_ms, "final_url": response.url, "tls_days_left": days, "warnings": warnings})
    except (requests.RequestException, OSError, ValueError) as exc:
        result["error"] = str(exc)
    return result


def markdown(results: list[dict]) -> str:
    lines = ["# Website Health Report", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", "", "| Status | URL | HTTP | Response | TLS days | Notes |", "|---|---|---:|---:|---:|---|"]
    for item in results:
        notes = "; ".join(item.get("warnings", [])) or item.get("error", "OK")
        lines.append(f"| {item['status']} | {item['url']} | {item.get('http_status', '-') } | {item.get('response_ms', '-')} ms | {item.get('tls_days_left', '-')} | {notes} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check authorized websites and create health reports")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("--markdown", default="report.md")
    parser.add_argument("--json", dest="json_path", default="report.json")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    results = [check_url(url, config.get("timeout_seconds", 10), config.get("slow_response_ms", 1500), config.get("tls_warning_days", 30)) for url in config["urls"]]
    Path(args.markdown).write_text(markdown(results), encoding="utf-8")
    Path(args.json_path).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(markdown(results))
    return 0 if all(item["status"] != "FAIL" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
