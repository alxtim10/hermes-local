"""Application service coordinating the Cryptocurrency domain."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from financial_tools.crypto.calculations import calculate_crypto_metrics
from financial_tools.crypto.provider import CryptoDataProvider, HybridCryptoProvider
from financial_tools.crypto.schemas import (
    CryptoAnalysisResponse,
    CryptoHistoryResponse,
    CryptoQuoteResponse,
)
from financial_tools.shared.security import validate_currency, validate_symbol


class CryptoService:
    """Service providing crypto quotes, historical series, and risk metrics."""

    def __init__(self, provider: Optional[CryptoDataProvider] = None):
        self.provider = provider or HybridCryptoProvider()

    async def get_crypto_quote(
        self,
        symbol: str,
        quote_currency: str = "USD",
    ) -> CryptoQuoteResponse:
        """Retrieves current crypto price and market metadata."""
        clean_sym = validate_symbol(symbol)
        clean_curr = validate_currency(quote_currency)
        return await self.provider.get_quote(clean_sym, clean_curr)

    async def get_crypto_history(
        self,
        symbol: str,
        quote_currency: str = "USD",
        days: int = 30,
    ) -> CryptoHistoryResponse:
        """Retrieves historical price series."""
        clean_sym = validate_symbol(symbol)
        clean_curr = validate_currency(quote_currency)
        return await self.provider.get_history(clean_sym, clean_curr, days=days)

    async def analyze_crypto(
        self,
        symbol: str,
        quote_currency: str = "USD",
        analysis_period: str = "30d",
    ) -> CryptoAnalysisResponse:
        """Computes return, volatility, and moving averages for cryptocurrency."""
        clean_sym = validate_symbol(symbol)
        clean_curr = validate_currency(quote_currency)

        days = 30
        if analysis_period.endswith("d"):
            try:
                days = int(analysis_period[:-1])
            except ValueError:
                pass
        elif analysis_period == "1y":
            days = 365

        history = await self.provider.get_history(clean_sym, clean_curr, days=days)
        latest_price = history.data[-1].price if history.data else Decimal("0.00")
        metrics = calculate_crypto_metrics(history.data)

        return CryptoAnalysisResponse(
            symbol=clean_sym,
            latest_price=latest_price,
            quote_currency=clean_curr,
            analysis_period=analysis_period,
            historical_return_pct=metrics.get("historical_return_pct"),
            volatility_metrics=metrics.get("volatility_metrics", {}),
            indicators=metrics.get("indicators", {}),
            data_source=history.provider,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
