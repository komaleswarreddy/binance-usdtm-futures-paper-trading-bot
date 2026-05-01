# Cross-verification: `file.md` (assignment) vs this repo

This document maps every requirement in [file.md](../file.md) (paths relative to repo root: `INternshala/file.md`) to what exists under `trading_bot/` and how it is verified.

## Objective & setup

| Requirement (file.md) | Status | Where / notes |
|----------------------|--------|----------------|
| Python app placing orders on Binance Futures Testnet (USDT-M) | Met | `bot/orders.py` + `binance-futures-connector` `UMFutures` |
| Reusable structure, logging, error handling | Met | Package layout; `logging_config.py`; `cli.py` catches validation, `ClientError`, `ServerError`, `RequestException` |
| Base URL `https://testnet.binancefuture.com` | Met | Set in `.env.example` and documented in README; also the default in `bot/client.py`; CLI `--base-url` can override if needed |
| Library: python-binance **or** REST | Met | Uses **`binance-futures-connector`** (REST client), allowed by spec |

## Core requirements (must-have)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Language Python 3.x | Met | Code + `README.md` prerequisites |
| Place **MARKET** and **LIMIT** on testnet USDT-M | Met | `place_market`, `place_limit` in `bot/orders.py` |
| **BUY** and **SELL** | Met | CLI `choices`; validators; passed through to API |
| CLI: symbol, side, type, quantity, price for LIMIT | Met | `cli.py` argparse + `validators.py` |
| Print order **request summary** | Met | `_print_order_summary` in `cli.py` |
| Print **response** orderId, status, executedQty, avgPrice (if present) | Met | `_print_response_details` prints those keys when API returns them |
| **Success / failure** message | Met | `Success: order accepted.` or stderr messages + exit codes |
| **Structured code**: client/API vs CLI | Met | `bot/client.py`, `bot/orders.py` vs `cli.py` |
| **Logging** to **log file** (requests/responses/errors) | Met | `setup_logging` + `logger.info` / `logger.exception` on submit and result; connector can log at DEBUG with `--verbose` |
| **Exception handling**: invalid input, API errors, network | Met | `ValueError` → exit 2; `ClientError`/`ServerError` → exit 1; `requests.RequestException` → exit 1 |

## Deliverables

| Deliverable | Status | Notes |
|-------------|--------|--------|
| Source code | Met | `trading_bot/` tree |
| **README.md**: setup, examples, assumptions | Met | [README.md](README.md) |
| **requirements.txt** | Met | [requirements.txt](requirements.txt) |
| Log files: one MARKET + one LIMIT | **You must generate** | Not committed (`.gitignore`). Run real CLI against testnet after `.env` is set; see README examples |

## Suggested structure (optional)

| Suggested path | Present |
|----------------|---------|
| `trading_bot/bot/__init__.py` | Yes |
| `trading_bot/bot/client.py` | Yes |
| `trading_bot/bot/orders.py` | Yes |
| `trading_bot/bot/validators.py` | Yes |
| `trading_bot/bot/logging_config.py` | Yes |
| `trading_bot/cli.py` | Yes |
| `trading_bot/README.md` | Yes |
| `trading_bot/requirements.txt` | Yes |

## Bonus (optional)

| Bonus | Status |
|-------|--------|
| Third order type (Stop-Limit / OCO / TWAP / Grid) | **Not implemented** (optional only) |
| Enhanced CLI UX | **Partial**: case-insensitive flags, clear validation/config errors; no full menu/prompt flow |
| Lightweight UI | Not implemented |

## Evaluation criteria (grading rubric)

| Criterion | How addressed |
|-----------|----------------|
| Correctness on testnet | Implementation matches Binance USDT-M futures `new_order`; **live** correctness requires your keys + valid sizes (automated tests **mock** the API) |
| Code quality / structure | Layered `bot/` + thin `cli.py` |
| Validation + error handling | `validators.py` + exit codes + tests in `tests/` |
| Logging | Rotating file + console; no secrets logged |
| README + runnable instructions | [README.md](README.md) + this file |

## Gaps / things automation does **not** prove

1. **Real testnet order** success — pytest uses mocks. You still run the two README commands with a funded testnet account.
2. **Exchange filters** (`LOT_SIZE`, `MIN_NOTIONAL`) — validated only by Binance when you submit; our CLI checks positivity and symbol shape.
3. **Submission zip / GitHub** — packaging is your step; contents are ready.

---

## How to run automated verification

From directory `trading_bot/`:

```bash
pip install -r requirements-dev.txt
pytest
```

Or on Windows PowerShell:

```powershell
.\run_tests.ps1
```

See [README.md — Automated tests](README.md#automated-tests) for details.
