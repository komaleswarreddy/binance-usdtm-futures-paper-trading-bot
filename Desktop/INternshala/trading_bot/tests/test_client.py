"""Tests for bot.client (file.md: testnet base URL)."""

import os
from unittest.mock import patch

import pytest

from bot.client import DEFAULT_TESTNET_BASE_URL, create_client


def test_create_client_requires_credentials():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="BINANCE_API_KEY"):
            create_client()


def test_create_client_uses_testnet_url_by_default():
    env = {"BINANCE_API_KEY": "k", "BINANCE_API_SECRET": "s"}
    with patch.dict(os.environ, env, clear=True):
        with patch("bot.client.UMFutures") as um:
            create_client()
            um.assert_called_once()
            call_kw = um.call_args.kwargs
            assert call_kw["base_url"] == DEFAULT_TESTNET_BASE_URL.rstrip("/")
            assert call_kw["key"] == "k"
            assert call_kw["secret"] == "s"


def test_create_client_uses_binance_base_url_from_env():
    custom_url = "https://example.testnet.local"
    with patch.dict(
        os.environ,
        {
            "BINANCE_API_KEY": "k",
            "BINANCE_API_SECRET": "s",
            "BINANCE_BASE_URL": custom_url,
        },
        clear=True,
    ):
        with patch("bot.client.UMFutures") as um:
            create_client()
            assert um.call_args.kwargs["base_url"] == custom_url


def test_default_base_url_matches_assignment_spec():
    assert DEFAULT_TESTNET_BASE_URL == "https://testnet.binancefuture.com"
