"""Pydantic schemas for the Cryptocurrency domain."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CryptoQuoteResponse(BaseModel):
    """Current price quote for cryptocurrency asset."""

    symbol: str
    current_price: Decimal
    quote_currency: str
    market_timestamp: str
    provider: str
    freshness_metadata: str
    market_cap_rank: Optional[int] = None
    change_24h_pct: Optional[float] = None


class CryptoPricePoint(BaseModel):
    """Historical timestamped price point."""

    timestamp: str
    price: Decimal


class CryptoHistoryResponse(BaseModel):
    """Historical price series for a cryptocurrency."""

    symbol: str
    quote_currency: str
    provider: str
    data_points_count: int
    data: List[CryptoPricePoint]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CryptoAnalysisResponse(BaseModel):
    """Analytical summary of historical return, volatility, and indicators."""

    symbol: str
    latest_price: Decimal
    quote_currency: str
    analysis_period: str
    historical_return_pct: Optional[float]
    volatility_metrics: Dict[str, Any]
    indicators: Dict[str, Any]
    data_source: str
    timestamp: str
    assumptions_and_limitations: str = (
        "Crypto markets operate 24/7 with high price volatility. Past realized returns "
        "and metrics must not be interpreted as guaranteed future profits or price stability."
    )
