import logging
from typing import Any

from binance.um_futures import UMFutures

logger = logging.getLogger(__name__)


def place_market(client: UMFutures, symbol: str, side: str, quantity: str) -> dict[str, Any]:
    logger.info(
        "Placing MARKET order symbol=%s side=%s quantity=%s",
        symbol,
        side,
        quantity,
    )
    return client.new_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity,
    )


def place_limit(
    client: UMFutures,
    symbol: str,
    side: str,
    quantity: str,
    price: str,
) -> dict[str, Any]:
    logger.info(
        "Placing LIMIT order symbol=%s side=%s quantity=%s price=%s",
        symbol,
        side,
        quantity,
        price,
    )
    return client.new_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        timeInForce="GTC",
        quantity=quantity,
        price=price,
    )
