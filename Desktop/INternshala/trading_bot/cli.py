"""
CLI entry point for Binance USDT-M Futures Testnet orders.
Run from the trading_bot directory: python cli.py --help
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

import requests
from binance.error import ClientError, ServerError
from dotenv import load_dotenv

from bot.client import DEFAULT_TESTNET_BASE_URL, create_client
from bot.logging_config import setup_logging
from bot.orders import place_limit, place_market
from bot.validators import (
    normalize_symbol,
    parse_price,
    parse_quantity,
    validate_order_type,
    validate_side,
)

logger = logging.getLogger(__name__)


def _print_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None,
) -> None:
    print("Order request summary:")
    print(f"  symbol: {symbol}")
    print(f"  side: {side}")
    print(f"  type: {order_type}")
    print(f"  quantity: {quantity}")
    if price is not None:
        print(f"  price: {price}")


def _print_response_details(resp: dict) -> None:
    print("Order response:")
    keys = ("orderId", "status", "executedQty", "avgPrice", "cumQty", "clientOrderId")
    for k in keys:
        if k in resp and resp[k] is not None:
            print(f"  {k}: {resp[k]}")


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance USDT-M Futures Testnet.",
    )
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument(
        "--side",
        required=True,
        type=str.upper,
        choices=["BUY", "SELL"],
    )
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        type=str.upper,
        choices=["MARKET", "LIMIT"],
        help="MARKET or LIMIT",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity (positive)")
    parser.add_argument(
        "--price",
        default=None,
        help="Limit price (required for LIMIT, omit for MARKET)",
    )
    parser.add_argument(
        "--log-file",
        default="logs/trading_bot.log",
        help="Log file path (default: logs/trading_bot.log)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="DEBUG logging",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help=f"API base URL (default: {DEFAULT_TESTNET_BASE_URL})",
    )

    args = parser.parse_args()
    setup_logging(args.log_file, verbose=args.verbose)

    try:
        symbol = normalize_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = parse_quantity(args.quantity)
        price: str | None = None
        if order_type == "LIMIT":
            if not args.price:
                raise ValueError("LIMIT orders require --price.")
            price = parse_price(args.price)
        elif args.price is not None:
            raise ValueError("--price must not be set for MARKET orders.")
    except ValueError as e:
        logger.warning("Validation failed: %s", e)
        print(f"Validation error: {e}", file=sys.stderr)
        return 2

    try:
        client = create_client(base_url=args.base_url)
    except ValueError as e:
        logger.error("Client configuration error: %s", e)
        print(f"Configuration error: {e}", file=sys.stderr)
        return 2

    _print_order_summary(symbol, side, order_type, quantity, price)
    logger.info(
        "Submitting order symbol=%s side=%s type=%s quantity=%s price=%s",
        symbol,
        side,
        order_type,
        quantity,
        price,
    )

    try:
        if order_type == "MARKET":
            resp = place_market(client, symbol, side, quantity)
        else:
            assert price is not None
            resp = place_limit(client, symbol, side, quantity, price)
    except ClientError as e:
        logger.exception(
            "Binance API client error status=%s code=%s msg=%s",
            getattr(e, "status_code", None),
            getattr(e, "error_code", None),
            getattr(e, "error_message", None),
        )
        print(
            f"API error (HTTP {getattr(e, 'status_code', '?')}): "
            f"code={getattr(e, 'error_code', '?')} "
            f"{getattr(e, 'error_message', e)}",
            file=sys.stderr,
        )
        return 1
    except ServerError as e:
        logger.exception("Binance server error: %s", getattr(e, "message", e))
        print(
            f"Binance server error (HTTP {e.status_code}): {e.message}",
            file=sys.stderr,
        )
        return 1
    except requests.RequestException as e:
        logger.exception("Network error: %s", e)
        print(
            f"Network error (check connectivity and firewall): {e}",
            file=sys.stderr,
        )
        return 1

    if not isinstance(resp, dict):
        resp = dict(resp) if hasattr(resp, "items") else {"data": resp}

    logger.info("Order success: %s", json.dumps(resp, default=str))
    _print_response_details(resp)
    print("Success: order accepted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
