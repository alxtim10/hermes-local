"""Common types and enums across domains."""

from decimal import Decimal
from enum import Enum
from typing import Annotated, Literal
from pydantic import PlainSerializer

try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

# Monetary representation: Decimal serialized to string with 2 decimal places by default
Money = Annotated[
    Decimal,
    PlainSerializer(lambda v: str(v.quantize(Decimal("0.01"))), return_type=str, when_used="json"),
]


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class MarketDataSource(str, Enum):
    YAHOO_FINANCE = "yahoo_finance"
    COINGECKO = "coingecko"
    BINANCE = "binance"
    INTERNAL_DB = "internal_db"
    MOCK = "mock_provider"


TechnicalIndicator = Literal[
    "SMA50",
    "SMA200",
    "EMA20",
    "RSI14",
    "MACD",
    "BOLLINGER_BANDS",
    "ATR14",
    "MAX_DRAWDOWN",
    "ANNUALIZED_VOLATILITY",
]
