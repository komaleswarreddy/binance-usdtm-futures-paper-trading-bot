import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(log_file: str, verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    abs_path = os.path.abspath(log_file)
    log_dir = os.path.dirname(abs_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    fh = RotatingFileHandler(
        abs_path, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(level)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    root.addHandler(ch)
