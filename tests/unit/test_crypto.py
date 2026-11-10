"""Unit tests for crypto domain calculations and provider normalization."""

from decimal import Decimal
import pytest
from financial_tools.crypto.calculations import calculate_crypto_metrics
from financial_tools.crypto.provider import MockCryptoProvider
from financial_tools.crypto.schemas import CryptoPricePoint
from financial_tools.crypto.service import CryptoService
from financial_tools.shared.exceptions import InvalidInputError
from financial_tools.shared.security import validate_currency


def test_currency_validation():
    assert validate_currency("usd") == "USD"
    assert validate_currency("idr") == "IDR"
    with pytest.raises(InvalidInputError):
        validate_currency("TOOLONG123")


def test_crypto_metrics_calculation():
    points = [
        CryptoPricePoint(timestamp=f"2026-10-{i:02d}", price=Decimal(str(p)))
        for i, p in enumerate([60000, 62000, 58000, 65000, 69000], 1)
    ]
    res = calculate_crypto_metrics(points)
    assert res["historical_return_pct"] == 15.0  # (69000 - 60000) / 60000 = 15%
    assert res["volatility_metrics"]["max_drawdown_pct"] < 0
    assert "annualized_volatility_pct" in res["volatility_metrics"]


@pytest.mark.asyncio
async def test_crypto_service_with_mock():
    provider = MockCryptoProvider(fixed_price=Decimal("65000.00"))
    service = CryptoService(provider=provider)

    quote = await service.get_crypto_quote("BTC", "USD")
    assert quote.symbol == "BTC"
    assert quote.current_price == Decimal("65000.00")
    assert quote.quote_currency == "USD"

    history = await service.get_crypto_history("BTC", "USD", days=14)
    assert history.data_points_count == 14

    analysis = await service.analyze_crypto("BTC", "USD", "30d")
    assert analysis.symbol == "BTC"
    assert analysis.historical_return_pct is not None
