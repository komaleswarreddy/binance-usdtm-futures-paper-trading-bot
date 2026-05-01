import re
from decimal import Decimal, InvalidOperation

SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]+USDT$")


def normalize_symbol(symbol: str) -> str:
    if not symbol or not str(symbol).strip():
        raise ValueError("symbol must not be empty.")
    s = str(symbol).strip().upper()
    if not SYMBOL_PATTERN.match(s):
        raise ValueError(
            "symbol must match pattern like BTCUSDT (alphanumeric + USDT suffix)."
        )
    return s


def validate_side(side: str) -> str:
    s = str(side).strip().upper()
    if s not in ("BUY", "SELL"):
        raise ValueError("side must be BUY or SELL.")
    return s


def validate_order_type(order_type: str) -> str:
    t = str(order_type).strip().upper()
    if t not in ("MARKET", "LIMIT"):
        raise ValueError("order type must be MARKET or LIMIT.")
    return t


def _decimal_to_api_string(d: Decimal) -> str:
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s if s else "0"


def parse_quantity(q: str) -> str:
    try:
        d = Decimal(str(q).strip())
    except InvalidOperation:
        raise ValueError("quantity must be a positive number.") from None
    if d <= 0:
        raise ValueError("quantity must be positive.")
    return _decimal_to_api_string(d)


def parse_price(p: str) -> str:
    try:
        d = Decimal(str(p).strip())
    except InvalidOperation:
        raise ValueError("price must be a positive number.") from None
    if d <= 0:
        raise ValueError("price must be positive.")
    return _decimal_to_api_string(d)
