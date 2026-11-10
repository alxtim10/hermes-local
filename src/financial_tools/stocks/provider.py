"""Stock market data provider interface and implementations."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import pandas as pd
import yfinance as yf

from financial_tools.shared.exceptions import (
    InvalidInputError,
    ProviderUnavailableError,
    ResourceNotFoundError,
)
from financial_tools.shared.logging import logger
from financial_tools.shared.security import validate_symbol
from financial_tools.stocks.schemas import (
    OHLCVDataPoint,
    StockHistoryResponse,
    StockQuoteResponse,
)


class StockDataProvider(ABC):
    """Abstract interface for stock market data sources."""

    @abstractmethod
    def get_quote(self, symbol: str, currency: Optional[str] = None) -> StockQuoteResponse:
        pass

    @abstractmethod
    def get_history(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d",
    ) -> StockHistoryResponse:
        pass


class YahooFinanceStockProvider(StockDataProvider):
    """Production provider using Yahoo Finance (supports US, IDX .JK, etc.)."""

    def get_quote(self, symbol: str, currency: Optional[str] = None) -> StockQuoteResponse:
        clean_symbol = validate_symbol(symbol)
        try:
            ticker = yf.Ticker(clean_symbol)
            # Fast info retrieval
            fast_info = getattr(ticker, "fast_info", None)
            price = None
            prev_close = None
            curr = currency or "USD"

            if fast_info:
                price = getattr(fast_info, "last_price", None)
                prev_close = getattr(fast_info, "previous_close", None)
                curr = getattr(fast_info, "currency", curr) or curr

            if price is None:
                # Fallback to history 1d
                hist = ticker.history(period="5d")
                if hist.empty:
                    raise ResourceNotFoundError(f"No market price found for stock ticker: {clean_symbol}")
                price = hist["Close"].iloc[-1]
                if len(hist) > 1:
                    prev_close = hist["Close"].iloc[-2]

            change_pct = None
            if price and prev_close:
                change_pct = round(float((price - prev_close) / prev_close * 100), 2)

            return StockQuoteResponse(
                symbol=clean_symbol,
                price=Decimal(str(round(float(price), 4))),
                currency=curr.upper(),
                market_timestamp=datetime.now(timezone.utc).isoformat(),
                data_source="yahoo_finance",
                data_freshness_information="Real-time or 15-min delayed exchange data via Yahoo Finance",
                previous_close=Decimal(str(round(float(prev_close), 4))) if prev_close else None,
                change_pct=change_pct,
            )
        except (ResourceNotFoundError, InvalidInputError):
            raise
        except Exception as exc:
            logger.error(f"YahooFinance quote error for {clean_symbol}: {exc}")
            raise ProviderUnavailableError(f"Failed to fetch stock quote for {clean_symbol}: {str(exc)}")

    def get_history(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d",
    ) -> StockHistoryResponse:
        clean_symbol = validate_symbol(symbol)
        try:
            ticker = yf.Ticker(clean_symbol)
            if start_date and end_date:
                hist = ticker.history(start=start_date, end=end_date, interval=interval)
            else:
                p = period or "1y"
                hist = ticker.history(period=p, interval=interval)

            if hist.empty:
                raise ResourceNotFoundError(f"No historical records found for stock ticker: {clean_symbol}")

            data_points: List[OHLCVDataPoint] = []
            for idx, row in hist.iterrows():
                ts = idx.isoformat() if hasattr(idx, "isoformat") else str(idx)
                data_points.append(
                    OHLCVDataPoint(
                        timestamp=ts,
                        open=Decimal(str(round(float(row["Open"]), 4))),
                        high=Decimal(str(round(float(row["High"]), 4))),
                        low=Decimal(str(round(float(row["Low"]), 4))),
                        close=Decimal(str(round(float(row["Close"]), 4))),
                        volume=int(row["Volume"]),
                    )
                )

            curr = getattr(ticker.fast_info, "currency", "USD") if hasattr(ticker, "fast_info") else "USD"

            return StockHistoryResponse(
                symbol=clean_symbol,
                currency=(curr or "USD").upper(),
                data_source="yahoo_finance",
                count=len(data_points),
                data=data_points,
                metadata={"interval": interval, "requested_period": period or f"{start_date} to {end_date}"},
            )
        except (ResourceNotFoundError, InvalidInputError):
            raise
        except Exception as exc:
            logger.error(f"YahooFinance history error for {clean_symbol}: {exc}")
            raise ProviderUnavailableError(f"Failed to fetch stock history for {clean_symbol}: {str(exc)}")


class MockStockProvider(StockDataProvider):
    """Mock provider for deterministic testing without external API calls."""

    def __init__(self, fixed_price: Decimal = Decimal("9500.00"), currency: str = "IDR"):
        self.fixed_price = fixed_price
        self.currency = currency

    def get_quote(self, symbol: str, currency: Optional[str] = None) -> StockQuoteResponse:
        clean = validate_symbol(symbol)
        return StockQuoteResponse(
            symbol=clean,
            price=self.fixed_price,
            currency=currency or self.currency,
            market_timestamp="2026-10-26T12:00:00Z",
            data_source="mock_provider",
            data_freshness_information="Simulated mock market data",
            previous_close=self.fixed_price - Decimal("50.00"),
            change_pct=0.53,
        )

    def get_history(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
        interval: str = "1d",
    ) -> StockHistoryResponse:
        clean = validate_symbol(symbol)
        data = [
            OHLCVDataPoint(
                timestamp=f"2026-10-2{i}T00:00:00Z",
                open=self.fixed_price,
                high=self.fixed_price + Decimal("100"),
                low=self.fixed_price - Decimal("100"),
                close=self.fixed_price + Decimal(f"{i * 10}"),
                volume=1000000,
            )
            for i in range(1, 6)
        ]
        return StockHistoryResponse(
            symbol=clean,
            currency=self.currency,
            data_source="mock_provider",
            count=len(data),
            data=data,
            metadata={"interval": interval},
        )
