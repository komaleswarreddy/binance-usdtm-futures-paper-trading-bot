"""CLI integration tests with mocks (no real Binance calls)."""

import sys
from unittest.mock import MagicMock

import pytest
import requests
from binance.error import ClientError, ServerError

import cli


@pytest.fixture(autouse=True)
def _no_dotenv_in_tests(monkeypatch):
    """Real .env would re-populate keys after delenv and can hit the network."""
    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: None)


def _mock_client_with_order_response(response: dict):
    client = MagicMock()
    client.new_order.return_value = response
    return client


@pytest.fixture
def env_keys(monkeypatch):
    monkeypatch.setenv("BINANCE_API_KEY", "test_key")
    monkeypatch.setenv("BINANCE_API_SECRET", "test_secret")


def test_main_market_success_prints_summary_and_success(env_keys, monkeypatch, capsys, tmp_path):
    client = _mock_client_with_order_response(
        {
            "orderId": 101,
            "status": "FILLED",
            "executedQty": "0.001",
            "avgPrice": "97000.5",
        }
    )
    monkeypatch.setattr(cli, "create_client", lambda **kw: client)

    log_file = tmp_path / "run.log"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "BUY",
            "--type",
            "MARKET",
            "--quantity",
            "0.001",
            "--log-file",
            str(log_file),
        ],
    )

    assert cli.main() == 0
    out = capsys.readouterr().out
    assert "Order request summary:" in out
    assert "BTCUSDT" in out and "BUY" in out and "MARKET" in out
    assert "Order response:" in out
    assert "orderId" in out and "101" in out
    assert "Success: order accepted." in out
    assert log_file.is_file()


def test_main_limit_requires_price(env_keys, monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "SELL",
            "--type",
            "LIMIT",
            "--quantity",
            "0.001",
            "--log-file",
            str(tmp_path / "x.log"),
        ],
    )
    assert cli.main() == 2
    assert "price" in capsys.readouterr().err.lower()


def test_main_market_rejects_price(env_keys, monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "BUY",
            "--type",
            "MARKET",
            "--quantity",
            "0.001",
            "--price",
            "1",
            "--log-file",
            str(tmp_path / "x.log"),
        ],
    )
    assert cli.main() == 2


def test_main_missing_api_keys(monkeypatch, capsys, tmp_path):
    monkeypatch.delenv("BINANCE_API_KEY", raising=False)
    monkeypatch.delenv("BINANCE_API_SECRET", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "BUY",
            "--type",
            "MARKET",
            "--quantity",
            "0.001",
            "--log-file",
            str(tmp_path / "x.log"),
        ],
    )
    assert cli.main() == 2
    assert "BINANCE_API_KEY" in capsys.readouterr().err


def test_main_client_error_exit_1(env_keys, monkeypatch, capsys, tmp_path):
    client = MagicMock()
    client.new_order.side_effect = ClientError(
        400, -2019, "Margin insufficient", {}
    )
    monkeypatch.setattr(cli, "create_client", lambda **kw: client)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "BUY",
            "--type",
            "MARKET",
            "--quantity",
            "0.001",
            "--log-file",
            str(tmp_path / "x.log"),
        ],
    )
    assert cli.main() == 1
    err = capsys.readouterr().err
    assert "API error" in err
    assert "400" in err


def test_main_server_error_exit_1(env_keys, monkeypatch, capsys, tmp_path):
    client = MagicMock()
    client.new_order.side_effect = ServerError(503, "Service unavailable")
    monkeypatch.setattr(cli, "create_client", lambda **kw: client)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "SELL",
            "--type",
            "MARKET",
            "--quantity",
            "0.001",
            "--log-file",
            str(tmp_path / "x.log"),
        ],
    )
    assert cli.main() == 1
    assert "server error" in capsys.readouterr().err.lower()


def test_main_network_error_exit_1(env_keys, monkeypatch, capsys, tmp_path):
    client = MagicMock()
    client.new_order.side_effect = requests.ConnectionError("no route")
    monkeypatch.setattr(cli, "create_client", lambda **kw: client)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "BUY",
            "--type",
            "MARKET",
            "--quantity",
            "0.001",
            "--log-file",
            str(tmp_path / "x.log"),
        ],
    )
    assert cli.main() == 1
    assert "Network error" in capsys.readouterr().err
