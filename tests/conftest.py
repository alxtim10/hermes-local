"""Pytest fixtures and isolated testing configuration."""

import pytest

from financial_tools.crypto.provider import MockCryptoProvider
from financial_tools.crypto.service import CryptoService
from financial_tools.stocks.provider import MockStockProvider
from financial_tools.stocks.service import StockService


@pytest.fixture
def mock_stock_service() -> StockService:
    return StockService(provider=MockStockProvider())


@pytest.fixture
def mock_crypto_service() -> CryptoService:
    return CryptoService(provider=MockCryptoProvider())
