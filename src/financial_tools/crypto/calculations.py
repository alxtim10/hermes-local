"""Volatility, return, and moving average metrics for cryptocurrencies."""

from typing import Any, Dict, List
import numpy as np
import pandas as pd

from financial_tools.crypto.schemas import CryptoPricePoint


def calculate_crypto_metrics(data_points: List[CryptoPricePoint]) -> Dict[str, Any]:
    """Calculates historical returns, 365-day annualized volatility, and drawdown."""
    if len(data_points) < 2:
        return {
            "historical_return_pct": None,
            "volatility_metrics": {"note": "Insufficient data points."},
            "indicators": {},
        }

    prices = pd.Series([float(p.price) for p in data_points])
    pct_changes = prices.pct_change().dropna()

    total_return_pct = round(((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100, 2)

    # Max Drawdown
    cum_max = prices.cummax()
    drawdown = (prices - cum_max) / cum_max
    max_drawdown_pct = round(float(drawdown.min() * 100), 2)

    # 365-day Annualized Volatility for crypto (24/7 market)
    ann_volatility_pct = (
        round(float(pct_changes.std() * np.sqrt(365) * 100), 2) if len(pct_changes) > 1 else None
    )

    # Moving averages if sufficient data
    indicators: Dict[str, Any] = {}
    if len(prices) >= 7:
        indicators["sma_7"] = round(float(prices.rolling(7).mean().iloc[-1]), 2)
    if len(prices) >= 30:
        indicators["sma_30"] = round(float(prices.rolling(30).mean().iloc[-1]), 2)
    if len(prices) >= 90:
        indicators["sma_90"] = round(float(prices.rolling(90).mean().iloc[-1]), 2)

    return {
        "historical_return_pct": total_return_pct,
        "volatility_metrics": {
            "annualized_volatility_pct": ann_volatility_pct,
            "max_drawdown_pct": max_drawdown_pct,
            "period_high": round(float(prices.max()), 2),
            "period_low": round(float(prices.min()), 2),
        },
        "indicators": indicators,
    }
