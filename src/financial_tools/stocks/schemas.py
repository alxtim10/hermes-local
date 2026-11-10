"""Pydantic schemas for the Stock domain."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StockQuoteResponse(BaseModel):
    """Real-time or latest available stock quote."""

    symbol: str
    price: Decimal
    currency: str
    market_timestamp: str
    data_source: str
    data_freshness_information: str
    previous_close: Optional[Decimal] = None
    change_pct: Optional[float] = None


class OHLCVDataPoint(BaseModel):
    """Single period OHLCV record."""

    timestamp: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class StockHistoryResponse(BaseModel):
    """Historical OHLCV series for a stock."""

    symbol: str
    currency: str
    data_source: str
    count: int
    data: List[OHLCVDataPoint]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StockAnalysisResponse(BaseModel):
    """Calculated technical, trend, and risk metrics for a stock."""

    symbol: str
    latest_price: Decimal
    currency: str
    analysis_period: str
    indicators: Dict[str, Any]
    risk_and_return_metrics: Dict[str, Any]
    data_source: str
    timestamp: str
    limitations_and_assumptions: str = (
        "Analytical metrics are computed from historical data and do NOT guarantee future performance. "
        "Missing price gaps or corporate actions may influence indicator precision."
    )
