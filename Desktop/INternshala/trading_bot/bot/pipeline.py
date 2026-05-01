"""Shared validate + submit flow for CLI and HTTP API."""

from __future__ import annotations

from typing import Any

from bot.client import create_client
from bot.orders import place_limit, place_market
from bot.validators import (
    normalize_symbol,
    parse_price,
    parse_quantity,
    validate_order_type,
    validate_side,
)


def parse_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None,
) -> tuple[str, str, str, str, str | None]:
    sym = normalize_symbol(symbol)
    side_v = validate_side(side)
    ot = validate_order_type(order_type)
    qty = parse_quantity(quantity)
    price_v: str | None = None
    if ot == "LIMIT":
        if not price:
            raise ValueError("LIMIT orders require a price.")
        price_v = parse_price(price)
    elif price is not None and str(price).strip():
        raise ValueError("price must not be set for MARKET orders.")
    return sym, side_v, ot, qty, price_v


def execute_parsed_order(
    sym: str,
    side_v: str,
    ot: str,
    qty: str,
    price_v: str | None,
    base_url: str | None = None,
) -> dict[str, Any]:
    client = create_client(base_url=base_url)
    if ot == "MARKET":
        raw = place_market(client, sym, side_v, qty)
    else:
        if price_v is None:
            raise ValueError("LIMIT orders require a price.")
        raw = place_limit(client, sym, side_v, qty, price_v)
    if not isinstance(raw, dict):
        return dict(raw) if hasattr(raw, "items") else {"data": raw}
    return raw
