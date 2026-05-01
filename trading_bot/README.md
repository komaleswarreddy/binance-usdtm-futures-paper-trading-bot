# Binance USDT-M Futures Testnet Trading Bot

Small Python CLI that places **MARKET** and **LIMIT** orders on Binance **USDT-M Futures Testnet**, with validation, logging to a file, and structured layers (`client` / `orders` / `validators` / CLI).

## Prerequisites

- Python **3.9+** (3.10+ recommended; matches `binance-futures-connector` support).
- A **Futures Testnet** account and API key pair.

## Setup

1. Register and log in at [https://testnet.binancefuture.com](https://testnet.binancefuture.com).
2. Open the **API Key** tab in the Futures Testnet UI and create key + secret.
3. Ensure the key is for **Futures Testnet** (not Spot Testnet, not Mainnet).

```bash
cd trading_bot
python -m venv .venv
```

**Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`  
**macOS/Linux:** `source .venv/bin/activate`

```bash
pip install -r requirements.txt
copy .env.example .env   # Windows: copy; Unix: cp
```

Edit `.env` and set:

- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`
- `BINANCE_BASE_URL=https://testnet.binancefuture.com`

You can still override per run if needed: `python cli.py ... --base-url https://...`

### Security (GitHub)

- **Never commit `.env`** — it is in `.gitignore`.
- If an API key or secret was shown in a screenshot, chat, or public repo, **revoke it on Binance** and create a new key.

## How to run

From the `trading_bot` directory:

```bash
python cli.py --help
```

### Examples

Use quantities and prices that satisfy the symbol’s **`LOT_SIZE`**, **`stepSize`**, and **`MIN_NOTIONAL`** on testnet. If Binance returns filter errors, reduce size or check exchange rules in the testnet UI / API.

**Market order** (writes to a dedicated log file for deliverables):

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --log-file logs/market_order.log
```

**Limit order:**

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000 --log-file logs/limit_order.log
```

`--side` and `--type` are case-insensitive (`buy` / `market` work).

**Debug logging** (more detail in the log file and console):

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001 --verbose
```

### Exit codes

| Code | Meaning |
|------|--------|
| 0 | Order submitted successfully |
| 1 | API or network error |
| 2 | Validation or configuration error (e.g. missing keys, LIMIT without `--price`) |

## Automated tests

Offline tests (mock Binance; no API keys needed):

```bash
cd trading_bot
pip install -r requirements-dev.txt
pytest
```

**Windows:** from `trading_bot`, run `.\run_tests.ps1` (installs dev deps and runs `pytest`).

**Linux/macOS:** `chmod +x run_tests.sh && ./run_tests.sh`

What the suite checks:

- Validators (symbol, side, type, quantity, price).
- `place_market` / `place_limit` call `new_order` with the right parameters (including `timeInForce=GTC` for limits).
- Default base URL is the assignment testnet URL.
- Logging writes to the configured log file.
- CLI prints request summary, response fields, success line; exit codes 0 / 1 / 2 for success, API/network, validation/config.

**Live testnet check** (optional, uses real keys and may place testnet orders):

1. Configure `.env` with futures testnet API key/secret.
2. Run the MARKET and LIMIT examples in [How to run](#how-to-run).
3. Confirm `logs/market_order.log` and `logs/limit_order.log` contain request/response lines and no secrets.

## Assignment cross-check (`file.md`)

- [VERIFY_ASSIGNMENT.md](VERIFY_ASSIGNMENT.md) — requirement checklist.
- [IMPLEMENTATION_MAP.md](IMPLEMENTATION_MAP.md) — **what they asked vs how we implemented** (end-to-end, for GitHub / viva).

## Project layout

```text
trading_bot/
  bot/
    __init__.py
    client.py          # UMFutures factory, testnet base URL
    orders.py          # MARKET / LIMIT placement
    validators.py      # Input validation
    logging_config.py  # File + console logging
  tests/               # pytest suite (run with requirements-dev.txt)
  cli.py
  requirements.txt
  requirements-dev.txt # adds pytest; includes -r requirements.txt
  pytest.ini
  run_tests.ps1 / run_tests.sh
  VERIFY_ASSIGNMENT.md # file.md requirement matrix
  logs/                # .gitkeep; *.log is gitignored — generate locally
```

## Deliverable log files

The assignment asks for logs from at least one MARKET and one LIMIT run. After configuring `.env`, run the two example commands above with `--log-file logs/market_order.log` and `logs/limit_order.log`. Log files are listed in `.gitignore` so they are not committed; keep copies for submission if required.

## Assumptions

- Testnet is available and API keys are created on **futures testnet**, not mainnet or spot testnet.
- Order parameters comply with Binance filters; the bot validates shape and positivity only, not exchange step sizes.
- Successful execution still depends on margin, price distance for limits, and testnet status.

## Dependencies

- [binance-futures-connector](https://pypi.org/project/binance-futures-connector/) (pinned in `requirements.txt`) — official-style REST client; pass `base_url` for testnet.
- `python-dotenv` — load `.env` for local development.
