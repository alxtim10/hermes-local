"""MCP tool registration for Cryptocurrency Domain."""

import json
import time
from typing import Any, Dict, Optional
from financial_tools.shared.types import FastMCP

from financial_tools.crypto.service import CryptoService
from financial_tools.shared.exceptions import FinancialToolsError
from financial_tools.shared.logging import log_tool_invocation


def register_crypto_tools(
    server: FastMCP,
    service: Optional[CryptoService] = None,
) -> None:
    """Registers cryptocurrency analysis tools on the FastMCP server."""
    app_service = service or CryptoService()

    @server.tool(
        name="get_crypto_quote",
        description=(
            "Retrieves current market price, quote currency, and metadata for a cryptocurrency symbol "
            "(e.g., 'BTC', 'ETH', 'SOL', 'BNB', 'USDT') against a quote currency (defaults to USD)."
        ),
    )
    async def get_crypto_quote(
        symbol: str,
        quote_currency: str = "USD",
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            res = await app_service.get_crypto_quote(symbol=symbol, quote_currency=quote_currency)
            log_tool_invocation("get_crypto_quote", (time.perf_counter() - start) * 1000, "success")
            return json.loads(res.model_dump_json())
        except (ValueError, FinancialToolsError) as exc:
            log_tool_invocation("get_crypto_quote", (time.perf_counter() - start) * 1000, "error")
            return {"error": str(exc), "status": "failed"}

    @server.tool(
        name="get_crypto_history",
        description=(
            "Fetches historical price series points for a cryptocurrency symbol over a designated number of days (e.g. 7, 30, 90)."
        ),
    )
    async def get_crypto_history(
        symbol: str,
        quote_currency: str = "USD",
        days: int = 30,
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            res = await app_service.get_crypto_history(
                symbol=symbol,
                quote_currency=quote_currency,
                days=days,
            )
            log_tool_invocation("get_crypto_history", (time.perf_counter() - start) * 1000, "success")
            return json.loads(res.model_dump_json())
        except Exception as exc:
            log_tool_invocation("get_crypto_history", (time.perf_counter() - start) * 1000, "error")
            return {"error": str(exc), "status": "failed"}

    @server.tool(
        name="analyze_crypto",
        description=(
            "Calculates historical percentage returns, annualized volatility (365-day basis), and moving averages "
            "for a cryptocurrency symbol over an analysis period (e.g., '30d', '90d', '365d')."
        ),
    )
    async def analyze_crypto(
        symbol: str,
        quote_currency: str = "USD",
        analysis_period: str = "30d",
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            res = await app_service.analyze_crypto(
                symbol=symbol,
                quote_currency=quote_currency,
                analysis_period=analysis_period,
            )
            log_tool_invocation("analyze_crypto", (time.perf_counter() - start) * 1000, "success")
            return json.loads(res.model_dump_json())
        except Exception as exc:
            log_tool_invocation("analyze_crypto", (time.perf_counter() - start) * 1000, "error")
            return {"error": str(exc), "status": "failed"}
