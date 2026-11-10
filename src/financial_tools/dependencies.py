"""Dependency factory and composition root for application services."""

from financial_tools.config import settings
from financial_tools.shared.http_client import ResilientHttpClient


def get_http_client() -> ResilientHttpClient:
    """Provides a configured resilient HTTP client."""
    return ResilientHttpClient(timeout_seconds=settings.crypto_api_timeout_seconds)
