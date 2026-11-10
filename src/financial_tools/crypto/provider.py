"""Cryptocurrency market data provider interface and implementations."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import yfinance as yf

from financial_tools.crypto.schemas import (
    CryptoHistoryResponse,
    CryptoPricePoint,
    CryptoQuoteResponse,
)
from financial_tools.shared.exceptions import (
    ProviderUnavailableError,
    RateLimitExceededError,
    ResourceNotFoundError,
)
from financial_tools.shared.http_client import ResilientHttpClient
from financial_tools.shared.logging import logger
from financial_tools.shared.security import validate_currency, validate_symbol

# Symbol normalization map to CoinGecko IDs
COINGECKO_ID_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "DOT": "polkadot",
    "AVAX": "avalanche-2",
    "LINK": "chainlink",
    "MATIC": "matic-network",
    "USDT": "tether",
    "USDC": "usd-coin",
}


class CryptoDataProvider(ABC):
    """Abstract interface for cryptocurrency data sources."""

    @abstractmethod
    async def get_quote(self, symbol: str, quote_currency: str = "USD") -> CryptoQuoteResponse:
        pass

    @abstractmethod
    async def get_history(
        self,
        symbol: str,
        quote_currency: str = "USD",
        days: int = 30,
    ) -> CryptoHistoryResponse:
        pass


class HybridCryptoProvider(CryptoDataProvider):
    """Primary CoinGecko provider with resilient fallback to Yahoo Finance for crypto tickers."""

    def __init__(
        self,
        http_client: Optional[ResilientHttpClient] = None,
        base_url: str = "https://api.coingecko.com/api/v3",
    ):
        self.http_client = http_client or ResilientHttpClient()
        self.base_url = base_url.rstrip("/")

    def _to_gecko_id(self, symbol: str) -> str:
        s = symbol.upper()
        return COINGECKO_ID_MAP.get(s, s.lower())

    async def get_quote(self, symbol: str, quote_currency: str = "USD") -> CryptoQuoteResponse:
        clean_symbol = validate_symbol(symbol)
        clean_quote = validate_currency(quote_currency)
        gecko_id = self._to_gecko_id(clean_symbol)

        try:
            url = f"{self.base_url}/simple/price"
            params = {
                "ids": gecko_id,
                "vs_currencies": clean_quote.lower(),
                "include_24hr_change": "true",
            }
            data = await self.http_client.get_json(url, params=params)
            if gecko_id in data and clean_quote.lower() in data[gecko_id]:
                price_val = data[gecko_id][clean_quote.lower()]
                change_24h = data[gecko_id].get(f"{clean_quote.lower()}_24h_change")
                return CryptoQuoteResponse(
                    symbol=clean_symbol,
                    current_price=Decimal(str(price_val)),
                    quote_currency=clean_quote,
                    market_timestamp=datetime.now(timezone.utc).isoformat(),
                    provider="coingecko",
                    freshness_metadata="Public real-time price feed via CoinGecko API",
                    change_24h_pct=round(float(change_24h), 2) if change_24h else None,
                )
        except Exception as exc:
            logger.warning(f"CoinGecko quote failed for {clean_symbol}, falling back to Yahoo Finance: {exc}")

        # Fallback to Yahoo Finance (e.g. BTC-USD)
        try:
            yf_ticker_sym = f"{clean_symbol}-{clean_quote}"
            ticker = yf.Ticker(yf_ticker_sym)
            hist = ticker.history(period="2d")
            if hist.empty:
                raise ResourceNotFoundError(f"Cryptocurrency quote not found for {clean_symbol}/{clean_quote}")

            last_price = float(hist["Close"].iloc[-1])
            prev_price = float(hist["Close"].iloc[-2]) if len(hist) > 1 else last_price
            chg = round(((last_price - prev_price) / prev_price) * 100, 2)

            return CryptoQuoteResponse(
                symbol=clean_symbol,
                current_price=Decimal(str(round(last_price, 4))),
                quote_currency=clean_quote,
                market_timestamp=datetime.now(timezone.utc).isoformat(),
                provider="yahoo_finance_crypto",
                freshness_metadata="Yahoo Finance Crypto 24/7 quote feed",
                change_24h_pct=chg,
            )
        except Exception as exc:
            raise ProviderUnavailableError(f"Could not retrieve crypto quote for {clean_symbol}: {str(exc)}")

    async def get_history(
        self,
        symbol: str,
        quote_currency: str = "USD",
        days: int = 30,
    ) -> CryptoHistoryResponse:
        clean_symbol = validate_symbol(symbol)
        clean_quote = validate_currency(quote_currency)
        gecko_id = self._to_gecko_id(clean_symbol)

        try:
            url = f"{self.base_url}/coins/{gecko_id}/market_chart"
            params = {"vs_currency": clean_quote.lower(), "days": str(days)}
            chart_data = await self.http_client.get_json(url, params=params)

            raw_prices = chart_data.get("prices", [])
            if raw_prices:
                points: List[CryptoPricePoint] = [
                    CryptoPricePoint(
                        timestamp=datetime.fromtimestamp(p[0] / 1000, tz=timezone.utc).isoformat(),
                        price=Decimal(str(round(float(p[1]), 4))),
                    )
                    for p in raw_prices
                ]
                return CryptoHistoryResponse(
                    symbol=clean_symbol,
                    quote_currency=clean_quote,
                    provider="coingecko",
                    data_points_count=len(points),
                    data=points,
                    metadata={"days": days},
                )
        except Exception as exc:
            logger.warning(f"CoinGecko history failed for {clean_symbol}, falling back to Yahoo Finance: {exc}")

        # Fallback to Yahoo Finance
        try:
            yf_sym = f"{clean_symbol}-{clean_quote}"
            period_str = f"{days}d" if days <= 60 else "1y"
            ticker = yf.Ticker(yf_sym)
            hist = ticker.history(period=period_str, interval="1d")
            if hist.empty:
                raise ResourceNotFoundError(f"Historical crypto series not found for {clean_symbol}")

            points = [
                CryptoPricePoint(
                    timestamp=idx.isoformat() if hasattr(idx, "isoformat") else str(idx),
                    price=Decimal(str(round(float(row["Close"]), 4))),
                )
                for idx, row in hist.iterrows()
            ]

            return CryptoHistoryResponse(
                symbol=clean_symbol,
                quote_currency=clean_quote,
                provider="yahoo_finance_crypto",
                data_points_count=len(points),
                data=points,
                metadata={"period": period_str},
            )
        except Exception as exc:
            raise ProviderUnavailableError(f"Could not retrieve crypto history for {clean_symbol}: {str(exc)}")


class MockCryptoProvider(CryptoDataProvider):
    """Mock crypto provider for testing."""

    def __init__(self, fixed_price: Decimal = Decimal("68500.00")):
        self.fixed_price = fixed_price

    async def get_quote(self, symbol: str, quote_currency: str = "USD") -> CryptoQuoteResponse:
        return CryptoQuoteResponse(
            symbol=symbol.upper(),
            current_price=self.fixed_price,
            quote_currency=quote_currency.upper(),
            market_timestamp="2026-10-26T12:00:00Z",
            provider="mock_crypto",
            freshness_metadata="Simulated price feed",
            change_24h_pct=2.45,
        )

    async def get_history(
        self,
        symbol: str,
        quote_currency: str = "USD",
        days: int = 30,
    ) -> CryptoHistoryResponse:
        points = [
            CryptoPricePoint(
                timestamp=f"2026-10-{i:02d}T00:00:00Z",
                price=self.fixed_price + Decimal(f"{i * 50}"),
            )
            for i in range(1, 15)
        ]
        return CryptoHistoryResponse(
            symbol=symbol.upper(),
            quote_currency=quote_currency.upper(),
            provider="mock_crypto",
            data_points_count=len(points),
            data=points,
            metadata={"days": days},
        )
