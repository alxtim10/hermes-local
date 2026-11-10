"""Unit tests for stock domain calculations and schemas."""

from decimal import Decimal
import pytest
from financial_tools.shared.exceptions import InvalidInputError
from financial_tools.shared.security import validate_symbol
from financial_tools.stocks.calculations import calculate_indicators, calculate_risk_metrics
from financial_tools.stocks.provider import MockStockProvider
from financial_tools.stocks.schemas import OHLCVDataPoint
from financial_tools.stocks.service import StockService


def test_symbol_validation():
    assert validate_symbol("bbca.jk") == "BBCA.JK"
    assert validate_symbol("aapl") == "AAPL"
    with pytest.raises(InvalidInputError):
        validate_symbol("INVALID;DROP TABLE;")


def test_calculate_risk_metrics():
    # 5 data points
    points = [
        OHLCVDataPoint(
            timestamp=f"2026-10-0{i}",
            open=Decimal("100"),
            high=Decimal("110"),
            low=Decimal("95"),
            close=Decimal(str(close_val)),
            volume=1000,
        )
        for i, close_val in enumerate([100.0, 105.0, 95.0, 110.0, 120.0], 1)
    ]
    res = calculate_risk_metrics(points)
    assert res["period_total_return_pct"] == 20.0  # (120 - 100) / 100 * 100 = 20%
    assert res["52_week_high"] == 120.0
    assert res["52_week_low"] == 95.0
    assert res["max_drawdown_pct"] < 0  # There was a drop from 105 to 95


def test_stock_service_with_mock():
    provider = MockStockProvider(fixed_price=Decimal("9500.00"), currency="IDR")
    service = StockService(provider=provider)

    quote = service.get_stock_quote("BBCA.JK")
    assert quote.symbol == "BBCA.JK"
    assert quote.price == Decimal("9500.00")
    assert quote.currency == "IDR"

    history = service.get_stock_history("BBCA.JK")
    assert history.count == 5
    assert len(history.data) == 5

    analysis = service.analyze_stock("BBCA.JK")
    assert analysis.symbol == "BBCA.JK"
    assert analysis.latest_price > Decimal("0")
    assert "period_total_return_pct" in analysis.risk_and_return_metrics
