"""Technical indicators, volatility, and risk metrics calculation for stocks."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from financial_tools.stocks.schemas import OHLCVDataPoint


def calculate_indicators(
    data_points: List[OHLCVDataPoint],
    requested_indicators: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Computes technical indicator values from OHLCV series."""
    if len(data_points) < 5:
        return {"note": "Insufficient historical points to compute full technical indicators (min 5 required)."}

    df = pd.DataFrame([
        {
            "open": float(p.open),
            "high": float(p.high),
            "low": float(p.low),
            "close": float(p.close),
            "volume": p.volume,
        }
        for p in data_points
    ])

    results: Dict[str, Any] = {}
    indicators = requested_indicators or ["SMA50", "SMA200", "RSI14", "MACD", "BOLLINGER_BANDS"]

    # Moving Averages
    if "SMA50" in indicators and len(df) >= 50:
        results["sma_50"] = round(float(df["close"].rolling(50).mean().iloc[-1]), 2)
    elif "SMA50" in indicators:
        results["sma_50"] = None

    if "SMA200" in indicators and len(df) >= 200:
        results["sma_200"] = round(float(df["close"].rolling(200).mean().iloc[-1]), 2)
    elif "SMA200" in indicators:
        results["sma_200"] = None

    if "EMA20" in indicators and len(df) >= 20:
        results["ema_20"] = round(float(df["close"].ewm(span=20, adjust=False).mean().iloc[-1]), 2)

    # Golden / Death Cross detection if both SMA50 & SMA200 available
    if results.get("sma_50") and results.get("sma_200"):
        results["trend_signal"] = (
            "Golden Cross (Bullish)" if results["sma_50"] > results["sma_200"] else "Death Cross (Bearish)"
        )

    # RSI 14
    if "RSI14" in indicators and len(df) >= 15:
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        val = rsi.iloc[-1]
        results["rsi_14"] = round(float(val), 2) if not np.isnan(val) else None
        if results["rsi_14"]:
            if results["rsi_14"] >= 70:
                results["rsi_signal"] = "Overbought (Potential Reversal/Pullback)"
            elif results["rsi_14"] <= 30:
                results["rsi_signal"] = "Oversold (Potential Bounce)"
            else:
                results["rsi_signal"] = "Neutral Momentum"

    # Bollinger Bands 20, 2
    if "BOLLINGER_BANDS" in indicators and len(df) >= 20:
        mid = df["close"].rolling(20).mean()
        std = df["close"].rolling(20).std()
        upper = mid + (2 * std)
        lower = mid - (2 * std)
        results["bollinger_bands"] = {
            "middle": round(float(mid.iloc[-1]), 2),
            "upper": round(float(upper.iloc[-1]), 2),
            "lower": round(float(lower.iloc[-1]), 2),
        }

    # MACD (12, 26, 9)
    if "MACD" in indicators and len(df) >= 35:
        ema12 = df["close"].ewm(span=12, adjust=False).mean()
        ema26 = df["close"].ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        hist = macd_line - signal_line
        results["macd"] = {
            "macd_line": round(float(macd_line.iloc[-1]), 4),
            "signal_line": round(float(signal_line.iloc[-1]), 4),
            "histogram": round(float(hist.iloc[-1]), 4),
            "momentum": "Bullish" if hist.iloc[-1] > 0 else "Bearish",
        }

    return results


def calculate_risk_metrics(data_points: List[OHLCVDataPoint]) -> Dict[str, Any]:
    """Calculates historical return, maximum drawdown, and volatility."""
    if len(data_points) < 2:
        return {"note": "Insufficient data to calculate risk metrics."}

    closes = pd.Series([float(p.close) for p in data_points])
    pct_changes = closes.pct_change().dropna()

    # Total return over period
    total_return_pct = round(((closes.iloc[-1] - closes.iloc[0]) / closes.iloc[0]) * 100, 2)

    # Max Drawdown
    cum_max = closes.cummax()
    drawdown = (closes - cum_max) / cum_max
    max_drawdown_pct = round(float(drawdown.min() * 100), 2)

    # Annualized Volatility (assuming 252 trading days)
    ann_volatility_pct = round(float(pct_changes.std() * np.sqrt(252) * 100), 2) if len(pct_changes) > 1 else None

    return {
        "period_total_return_pct": total_return_pct,
        "max_drawdown_pct": max_drawdown_pct,
        "annualized_volatility_pct": ann_volatility_pct,
        "52_week_high": round(float(closes.max()), 2),
        "52_week_low": round(float(closes.min()), 2),
    }
