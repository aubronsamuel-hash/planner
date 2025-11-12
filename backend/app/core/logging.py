"""Shared logging helpers for Planner services."""
from __future__ import annotations

import logging
import os

_logger_initialised = False


def configure_logging(service_name: str) -> None:
    """Attach a Loki handler when configuration is provided."""

    global _logger_initialised
    if _logger_initialised:
        return

    logging.basicConfig(level=os.getenv("PLANNER_LOG_LEVEL", "INFO"))
    loki_url = os.getenv("PLANNER_LOKI_URL")
    if loki_url:
        from logging_loki import LokiQueueHandler

        handler = LokiQueueHandler(
            url=loki_url,
            tags={"service": service_name},
            version="1",
        )
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
    _logger_initialised = True


__all__ = ["configure_logging"]
