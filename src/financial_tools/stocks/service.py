"""Application service coordinating the Stock domain."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from financial_tools.shared.security import validate_symbol
from financial_tools.stocks.calculations import calculate_indicators, calculate_risk_metrics
from financial_tools.stocks.provider import StockDataProvider, YahooFinanceStockProvider
from financial_tools.stocks.schemas import (
    StockAnalysisResponse,
    StockHistoryResponse,
    StockQuoteResponse,
)


class StockService:
    """Service providing stock quotes, history, and technical analysis."""

    def __init__(self, provider: Optional[StockDataProvider] = None):
        self.provider = provider or YahooFinanceStockProvider()

    def get_stock_quote(self, symbol: str, currency: Optional[str] = None) -> StockQuoteResponse:
        """Retrieves real-time or latest available stock quote."""
        clean = validate_symbol(symbol)
        return self.provider.get_quote(clean, currency)

    def get_stock_history(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "1d",
    ) -> StockHistoryResponse:
        """Retrieves historical OHLCV data series."""
        clean = validate_symbol(symbol)
        return self.provider.get_history(
            symbol=clean,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
        )

    def analyze_stock(
        self,
        symbol: str,
        analysis_period: str = "1y",
        indicators: Optional[List[str]] = None,
    ) -> StockAnalysisResponse:
        """Computes technical indicators and volatility metrics from historical data."""
        clean = validate_symbol(symbol)
        history = self.provider.get_history(symbol=clean, period=analysis_period)
        latest_price = history.data[-1].close if history.data else Decimal("0.00")

        ind_results = calculate_indicators(history.data, indicators)
        risk_results = calculate_risk_metrics(history.data)

        return StockAnalysisResponse(
            symbol=clean,
            latest_price=latest_price,
            currency=history.currency,
            analysis_period=analysis_period,
            indicators=ind_results,
            risk_and_return_metrics=risk_results,
            data_source=history.data_source,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
