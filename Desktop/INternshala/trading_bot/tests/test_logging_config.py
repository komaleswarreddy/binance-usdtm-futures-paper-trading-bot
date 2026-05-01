"""Tests for bot.logging_config (file.md: log to file)."""

import logging

from bot.logging_config import setup_logging


def test_setup_logging_creates_file(tmp_path):
    log_path = tmp_path / "nested" / "app.log"
    setup_logging(str(log_path), verbose=False)

    logging.getLogger("test_logger").info("hello")
    logging.shutdown()

    assert log_path.is_file()
    text = log_path.read_text(encoding="utf-8")
    assert "hello" in text
