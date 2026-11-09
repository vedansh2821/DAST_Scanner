#!/usr/bin/env python3
"""DAST_Scanner — a small demo wrapper around OWASP ZAP.

For authorised testing only: only scan systems you own or have written
permission to test. This script does nothing on its own — it requires a
running OWASP ZAP instance and talks to it over the ZAP API.

Usage:
    python scanner.py --target https://example.com --output report.json
"""

import argparse
import json
import sys
import time

try:
    from zapv2 import ZAPv2
except ImportError:  # python-owasp-zap-v2.4 not installed
    ZAPv2 = None


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Demo OWASP ZAP DAST scanner (authorised use only)."
    )
    parser.add_argument("--target", required=True,
                        help="Target URL to scan (http:// or https://).")
    parser.add_argument("--output", default="report.json",
                        help="Path to write the JSON alert report.")
    parser.add_argument("--zap-url", default="http://127.0.0.1:8080",
                        help="OWASP ZAP API base URL.")
    parser.add_argument("--api-key", default="",
                        help="ZAP API key, if configured.")
    parser.add_argument("--spider-timeout", type=int, default=120,
                        help="Seconds to wait for the spider (default 120).")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if not args.target.startswith(("http://", "https://")):
        print(f"error: --target must start with http:// or https:// "
              f"(got {args.target!r})", file=sys.stderr)
        return 2

    if ZAPv2 is None:
        print("error: python-owasp-zap-v2.4 is not installed. "
              "Run: pip install -r requirements.txt", file=sys.stderr)
        return 2

    print(f"Connecting to ZAP at {args.zap_url} ...")
    zap = ZAPv2(apikey=args.api_key,
                proxies={"http": args.zap_url, "https": args.zap_url})
    try:
        version = zap.core.version
    except Exception as exc:  # ZAP not running / unreachable
        print(f"error: could not reach ZAP at {args.zap_url}: {exc}",
              file=sys.stderr)
        print("Start OWASP ZAP first (GUI or daemon mode) and try again.",
              file=sys.stderr)
        return 1
    print(f"Connected to ZAP version {version}")

    print(f"Spidering {args.target} ...")
    try:
        scan_id = zap.spider.scan(args.target)
    except Exception as exc:
        print(f"error: failed to start spider: {exc}", file=sys.stderr)
        return 1

    deadline = time.time() + args.spider_timeout
    while time.time() < deadline:
        status = int(zap.spider.status(scan_id))
        print(f"  spider progress: {status}%")
        if status >= 100:
            break
        time.sleep(5)
    else:
        print("warning: spider timed out; continuing with partial results",
              file=sys.stderr)

    alerts = zap.core.alerts(baseurl=args.target)
    print(f"Found {len(alerts)} alert(s). Writing report to {args.output}")
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump({"target": args.target, "zap_version": version,
                   "alerts": alerts}, fh, indent=2)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
