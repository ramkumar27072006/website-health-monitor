import json
from pathlib import Path

from monitor import markdown


def test_markdown_contains_summary():
    report = markdown([{"url": "https://example.com", "status": "PASS", "http_status": 200, "response_ms": 120, "tls_days_left": 90, "warnings": []}])
    assert "Website Health Report" in report
    assert "example.com" in report


def test_example_config_is_valid():
    config = json.loads(Path("config.example.json").read_text())
    assert config["urls"]
