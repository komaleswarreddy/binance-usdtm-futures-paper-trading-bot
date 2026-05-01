# What the assignment asked for vs what we implemented

This maps [file.md](../file.md) (Internshala task) to this repository. Use it for README-style explanations or viva notes.

## Objective

| Asked | Implemented |
|-------|-------------|
| Small Python app that places orders on Binance Futures **Testnet** (USDT-M), clean structure, logging, error handling | `trading_bot/` package: `bot/client.py`, `bot/orders.py`, `bot/validators.py`, `bot/logging_config.py`, `cli.py` |

## Setup (assignment text)

| Asked | Implemented |
|-------|-------------|
| Register testnet, generate API credentials | Documented in [README.md](README.md); credentials via `.env` (`BINANCE_API_KEY`, `BINANCE_API_SECRET`) |
| Base URL `https://testnet.binancefuture.com` | Implemented as default in [bot/client.py](bot/client.py), and documented in `.env.example` / README. |
| python-binance **or** REST | **REST** via official-style client: `binance-futures-connector` (`UMFutures`), which calls the same HTTP API |

## Core requirements

| Asked | Implemented |
|-------|-------------|
| Python 3.x | Code + README; tests run on 3.9+ |
| MARKET and LIMIT orders, USDT-M | `place_market`, `place_limit` in [bot/orders.py](bot/orders.py); LIMIT uses `timeInForce=GTC` |
| BUY and SELL | CLI choices + validators |
| CLI: symbol, side, type, quantity, price for LIMIT | [cli.py](cli.py) + [bot/validators.py](bot/validators.py) |
| Print request summary, response (orderId, status, executedQty, avgPrice when present), success/failure | `_print_order_summary`, `_print_response_details`, exit **0** + success line or stderr + exit **1** / **2** |
| Separate client/API layer and CLI | `bot/*` vs `cli.py` |
| Log requests, responses, errors to a **file** | [bot/logging_config.py](bot/logging_config.py); `logger.info` / `logger.exception` in CLI and orders |
| Handle invalid input, API errors, network | `ValueError` → 2; `ClientError` / `ServerError` → 1; `requests.RequestException` → 1 |

## Deliverables

| Asked | Implemented |
|-------|-------------|
| Source + README (setup, examples, assumptions) + `requirements.txt` | Present under `trading_bot/` |
| Log files: one MARKET, one LIMIT | **You generate** after `.env` is set: see README example commands with `--log-file`; logs are gitignored |
| GitHub or zip | You push repo; **never commit `.env`** (listed in `.gitignore`) |

## Optional bonus (file.md)

| Bonus | Status |
|-------|--------|
| Extra order types / menus / UI | Not required; partial UX: case-insensitive CLI flags, clear errors |

## Evaluation criteria (how graders map to repo)

| Criterion | Evidence |
|-----------|----------|
| Correctness on testnet | Run real `cli.py` with Futures Testnet keys and `https://testnet.binancefuture.com`; automated tests mock API |
| Code quality | Layered modules, typed helpers |
| Validation + errors | `validators.py` + `tests/` |
| Logging | Rotating file + console; secrets not logged |
| Clear README | [README.md](README.md), [VERIFY_ASSIGNMENT.md](VERIFY_ASSIGNMENT.md), this file |

## Environment variables (local)

| Variable | Role |
|----------|------|
| `BINANCE_API_KEY` | API key from Binance Futures Testnet |
| `BINANCE_API_SECRET` | Secret |
| `BINANCE_BASE_URL` | Set to `https://testnet.binancefuture.com` to match assignment |
| CLI `--base-url` | Overrides both default and `BINANCE_BASE_URL` |

## Security

- **Do not commit `.env`** or paste live keys into GitHub issues, screenshots shared publicly, or this markdown file.
- If keys were ever exposed, **delete the API key in Binance** and create a new one.
