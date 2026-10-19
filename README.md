# Website Health Monitor

A lightweight, privacy-friendly Python tool for checking website availability, response time, TLS certificate expiry, and security headers.

## Why it is useful

Small businesses often discover downtime only after customers complain. This tool creates a simple report that can be run manually or scheduled with cron/Task Scheduler.

## Features

- Checks HTTP status and response time
- Follows redirects and records the final URL
- Checks TLS certificate expiry for HTTPS sites
- Checks common security headers
- Outputs Markdown and JSON reports
- No account, database, or third-party service required
- Safe by design: one request per configured URL

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.json config.json
python3 monitor.py --config config.json --markdown report.md --json report.json
```

Edit `config.json` and add websites you own or are authorized to monitor.

## Example output

```text
PASS  https://example.com  200  241ms  TLS 88 days left
WARN  https://shop.example  200  510ms  Missing: Content-Security-Policy
FAIL  https://offline.example  connection error
```

## Scheduling

Run every 15 minutes with cron:

```cron
*/15 * * * * cd /path/to/website-health-monitor && .venv/bin/python monitor.py --config config.json --markdown report.md --json report.json
```

## Responsible use

Only monitor websites you own or have explicit permission to monitor. This project is an availability and configuration checker, not a vulnerability scanner.

## Possible paid services

This tool can support a small service offering: website health setup, monthly monitoring reports, SSL-expiry reminders, and basic security-header improvements. Do not promise guaranteed uptime or security.

## License

MIT
