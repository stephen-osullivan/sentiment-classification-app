# src/logging_config.py
import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure root logging for the application.

    Safe to call multiple times.
    """
    root_logger = logging.getLogger()

    if root_logger.handlers:
        # Logging already configured (e.g. by uvicorn, pytest)
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger.setLevel(level)
    root_logger.addHandler(handler)