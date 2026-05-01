"""Unit tests for bot.orders (file.md: MARKET/LIMIT on USDT-M)."""

from unittest.mock import MagicMock

from bot.orders import place_limit, place_market


def test_place_market_delegates_to_client():
    client = MagicMock()
    client.new_order.return_value = {"orderId": 1, "status": "NEW"}

    out = place_market(client, "BTCUSDT", "SELL", "0.002")

    client.new_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="SELL",
        type="MARKET",
        quantity="0.002",
    )
    assert out["orderId"] == 1


def test_place_limit_includes_time_in_force_gtc():
    client = MagicMock()
    client.new_order.return_value = {"orderId": 2, "status": "NEW"}

    out = place_limit(client, "BTCUSDT", "BUY", "0.001", "42000")

    client.new_order.assert_called_once_with(
        symbol="BTCUSDT",
        side="BUY",
        type="LIMIT",
        timeInForce="GTC",
        quantity="0.001",
        price="42000",
    )
    assert out["orderId"] == 2
