"""Unit tests for bot.validators (file.md: CLI input validation)."""

import pytest

from bot.validators import (
    normalize_symbol,
    parse_price,
    parse_quantity,
    validate_order_type,
    validate_side,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("btcusdt", "BTCUSDT"),
        ("  ETHUSDT ", "ETHUSDT"),
    ],
)
def test_normalize_symbol_ok(raw, expected):
    assert normalize_symbol(raw) == expected


@pytest.mark.parametrize(
    "raw",
    ["", "  ", "BTC-PERP", "BTCUSD", "INVALID"],
)
def test_normalize_symbol_rejects(raw):
    with pytest.raises(ValueError):
        normalize_symbol(raw)


@pytest.mark.parametrize("side", ["BUY", "SELL", "buy", " sell "])
def test_validate_side_ok(side):
    assert validate_side(side) in ("BUY", "SELL")


@pytest.mark.parametrize("side", ["HOLD", "", "LONG"])
def test_validate_side_rejects(side):
    with pytest.raises(ValueError, match="BUY or SELL"):
        validate_side(side)


@pytest.mark.parametrize("t", ["MARKET", "LIMIT", "market"])
def test_validate_order_type_ok(t):
    assert validate_order_type(t) in ("MARKET", "LIMIT")


@pytest.mark.parametrize("t", ["STOP", ""])
def test_validate_order_type_rejects(t):
    with pytest.raises(ValueError, match="MARKET or LIMIT"):
        validate_order_type(t)


@pytest.mark.parametrize("q,expected", [("0.001", "0.001"), ("1", "1"), ("  2.5  ", "2.5")])
def test_parse_quantity_ok(q, expected):
    assert parse_quantity(q) == expected


@pytest.mark.parametrize("q", ["0", "-1", "abc", ""])
def test_parse_quantity_rejects(q):
    with pytest.raises(ValueError):
        parse_quantity(q)


@pytest.mark.parametrize("p,expected", [("50000", "50000"), ("0.01", "0.01")])
def test_parse_price_ok(p, expected):
    assert parse_price(p) == expected


@pytest.mark.parametrize("p", ["0", "-5", "x"])
def test_parse_price_rejects(p):
    with pytest.raises(ValueError):
        parse_price(p)
