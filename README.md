# DAST_Scanner

A small, clean **demo** wrapper around [OWASP ZAP](https://www.zaproxy.org/) for
dynamic application security testing (DAST).

> **⚠️ For authorised testing only — only scan systems you own or have written permission to test.**
> Unauthorised scanning may be illegal. This project is a starter/demo, not a
> production scanner, and it does nothing without a running ZAP instance.

## How it works

`scanner.py` talks to a locally running ZAP instance over its API:

1. Starts a spider against `--target`.
2. Waits for the spider to finish.
3. Fetches the alerts ZAP found and writes them as JSON to `--output`.

If ZAP is not running, the script exits with a clear error instead of
pretending to scan anything.

## Requirements

- Python 3.10+
- A running OWASP ZAP instance (default API URL `http://127.0.0.1:8080`)
- Dependencies in `requirements.txt`

## Usage

```bash
pip install -r requirements.txt

# Start ZAP first (GUI or daemon mode), then run:
python scanner.py --target https://example.com --output report.json
```

Options:

| Flag | Default | Description |
| --- | --- | --- |
| `--target` | *(required)* | URL to scan (must start with `http://` or `https://`) |
| `--output` | `report.json` | Where to write the JSON alert report |
| `--zap-url` | `http://127.0.0.1:8080` | ZAP API base URL |
| `--api-key` | *(none)* | ZAP API key, if ZAP is configured with one |

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs `python -m py_compile scanner.py`
on every push and pull request.

## License

MIT. Use responsibly and only with authorisation.
