# Website Health Monitor

A lightweight, privacy-friendly Python tool for checking website availability, response time, TLS certificate expiry, and security headers.

## Why it is useful

Small businesses often discover downtime only after customers complain. This tool creates a simple report that can be run manually or scheduled with cron/Task Scheduler.

## Customer use case

Local restaurants, clinics, coaching centers, and online shops may not notice when their website is slow or offline. A freelancer can configure this monitor, send a weekly report, and remind the owner about problems such as downtime, missing headers, or an expiring TLS certificate.

This is a service tool, not passive income by itself. The value comes from setup, maintenance, reporting, and helping the customer fix issues.

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

This tool can support a small service offering:

| Offer | Example starting price | Deliverable |
|---|---:|---|
| One-time setup | ₹499–₹1,999 | Configure URLs and schedule checks |
| Monthly monitoring | ₹499–₹2,999/month | Reports, review, and reminders |
| Website health review | ₹999–₹4,999 | Explain failures and recommend fixes |

These are example prices, not guaranteed earnings. Find customers through local businesses, LinkedIn, WhatsApp contacts, freelance marketplaces, or a short live demo. Never promise guaranteed uptime or security.

## Customer demo

Open [`demo.html`](demo.html) in a browser for a customer-friendly report preview. It is a static sample based on the same report fields produced by the command-line tool; it does not claim to monitor anything until configured and run.

Suggested outreach message:

> I can monitor your website for downtime, slow responses, and SSL-expiry risks and send you a simple monthly report. I can set up a free one-day trial using only your public website URL, then you can decide whether the service is useful.

## License

MIT
