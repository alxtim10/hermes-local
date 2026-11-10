"""Structured logging configuration for Financial Tools.

Diagnostic and trace logs are strictly routed to stderr so that MCP stdio transport
remains clean and uninterrupted on stdout.
"""

import logging
import sys
from typing import Any, Dict, Optional


def setup_logging(level_name: str = "INFO") -> logging.Logger:
    """Configures structured stderr logging."""
    logger = logging.getLogger("financial_tools")
    logger.setLevel(getattr(logging, level_name.upper(), logging.INFO))

    # Avoid duplicate handlers if re-called
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging()


def log_tool_invocation(
    tool_name: str,
    duration_ms: float,
    status: str,
    correlation_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """Logs tool execution metadata without leaking sensitive data."""
    msg = f"tool={tool_name} status={status} duration_ms={duration_ms:.2f}"
    if correlation_id:
        msg += f" correlation_id={correlation_id}"
    if extra:
        sanitized = {
            k: v for k, v in extra.items()
            if not any(secret in k.lower() for secret in ["key", "secret", "password", "token"])
        }
        msg += f" extra={sanitized}"
    logger.info(msg)
