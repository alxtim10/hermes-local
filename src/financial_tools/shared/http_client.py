"""Resilient HTTP client wrapper for market data providers."""

import asyncio
from typing import Any, Dict, Optional
import httpx
from financial_tools.shared.exceptions import (
    ProviderUnavailableError,
    RateLimitExceededError,
)
from financial_tools.shared.logging import logger


class ResilientHttpClient:
    """Async HTTP client with timeout, retry backoff, and rate limit awareness."""

    def __init__(self, timeout_seconds: float = 15.0, max_retries: int = 2):
        self.timeout = httpx.Timeout(timeout_seconds, connect=5.0)
        self.max_retries = max_retries

    async def get_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Executes GET request with bounded exponential backoff for transient errors."""
        attempt = 0
        backoff = 0.5

        while attempt <= self.max_retries:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, params=params, headers=headers)

                    if response.status_code == 429:
                        raise RateLimitExceededError(
                            f"Provider rate limit exceeded for URL: {url}"
                        )
                    if response.status_code >= 500:
                        raise ProviderUnavailableError(
                            f"Provider returned server error ({response.status_code}) for URL: {url}"
                        )

                    response.raise_for_status()
                    return response.json()

            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                attempt += 1
                if attempt > self.max_retries:
                    logger.warning(f"HTTP request failed after {self.max_retries} retries: {url}")
                    raise ProviderUnavailableError(f"Provider unreachable: {str(exc)}")
                logger.debug(f"Transient HTTP failure, retrying in {backoff}s: {url}")
                await asyncio.sleep(backoff)
                backoff *= 2
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 429:
                    raise RateLimitExceededError(f"Rate limit exceeded: {exc}")
                raise ProviderUnavailableError(f"Provider HTTP error: {exc}")
