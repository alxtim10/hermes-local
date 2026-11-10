"""MCP tool registration for Stock Domain."""

import json
import time
from typing import Any, Dict, List, Optional
from financial_tools.shared.types import FastMCP

from financial_tools.shared.exceptions import FinancialToolsError
from financial_tools.shared.logging import log_tool_invocation
from financial_tools.stocks.service import StockService


def register_stock_tools(
    server: FastMCP,
    service: Optional[StockService] = None,
) -> None:
    """Registers stock analysis tools on the FastMCP server."""
    app_service = service or StockService()

    @server.tool(
        name="get_stock_quote",
        description=(
            "Retrieves current market price, exchange currency, and data freshness metadata for a stock symbol "
            "(e.g., 'BBCA.JK' for Bank Central Asia on IDX, 'AAPL', 'NVDA', 'TLKM.JK')."
        ),
    )
    def get_stock_quote(
        symbol: str,
        currency: Optional[str] = None,
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            res = app_service.get_stock_quote(symbol=symbol, currency=currency)
            log_tool_invocation("get_stock_quote", (time.perf_counter() - start) * 1000, "success")
            return json.loads(res.model_dump_json())
        except (ValueError, FinancialToolsError) as exc:
            log_tool_invocation("get_stock_quote", (time.perf_counter() - start) * 1000, "error")
            return {"error": str(exc), "status": "failed"}

    @server.tool(
        name="get_stock_history",
        description=(
            "Fetches historical OHLCV (Open, High, Low, Close, Volume) data series for a given stock symbol "
            "over a specified start_date and end_date (YYYY-MM-DD)."
        ),
    )
    def get_stock_history(
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d",
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            res = app_service.get_stock_history(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                interval=interval,
            )
            log_tool_invocation("get_stock_history", (time.perf_counter() - start) * 1000, "success")
            return json.loads(res.model_dump_json())
        except Exception as exc:
            log_tool_invocation("get_stock_history", (time.perf_counter() - start) * 1000, "error")
            return {"error": str(exc), "status": "failed"}

    @server.tool(
        name="analyze_stock",
        description=(
            "Calculates technical indicators (SMA50, SMA200, RSI14, MACD, Bollinger Bands) "
            "and historical risk metrics (Max Drawdown, Volatility) for a stock symbol over an analysis period (e.g. '1y', '6m')."
        ),
    )
    def analyze_stock(
        symbol: str,
        analysis_period: str = "1y",
        indicators: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            res = app_service.analyze_stock(
                symbol=symbol,
                analysis_period=analysis_period,
                indicators=indicators,
            )
            log_tool_invocation("analyze_stock", (time.perf_counter() - start) * 1000, "success")
            return json.loads(res.model_dump_json())
        except Exception as exc:
            log_tool_invocation("analyze_stock", (time.perf_counter() - start) * 1000, "error")
            return {"error": str(exc), "status": "failed"}
