import os
from typing import Optional

from binance.um_futures import UMFutures

DEFAULT_TESTNET_BASE_URL = "https://testnet.binancefuture.com"


def create_client(
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    base_url: Optional[str] = None,
) -> UMFutures:
    key = api_key or os.environ.get("BINANCE_API_KEY")
    secret = api_secret or os.environ.get("BINANCE_API_SECRET")
    if not key or not secret:
        raise ValueError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set (environment variables or .env file)."
        )
    # CLI --base-url wins; else .env BINANCE_BASE_URL; else classic testnet (assignment default).
    url = (
        base_url
        or os.environ.get("BINANCE_BASE_URL")
        or DEFAULT_TESTNET_BASE_URL
    ).rstrip("/")
    return UMFutures(key=key, secret=secret, base_url=url)
