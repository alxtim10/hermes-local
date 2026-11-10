# MCP Tool Catalog

Complete reference for all 11 MCP tools exposed by the Financial Agent Tools server.

---

## Stock Domain

### `get_stock_quote`

Retrieves current market price for a stock symbol.

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | ✅ | Stock ticker (e.g., `BBCA.JK`, `AAPL`, `NVDA`) |
| `currency` | string | ❌ | Override quote currency |

**Output:**
```json
{
  "symbol": "BBCA.JK",
  "price": "9575.00",
  "currency": "IDR",
  "market_timestamp": "2026-10-26T08:00:00Z",
  "data_source": "yahoo_finance",
  "data_freshness_information": "Real-time or 15-min delayed exchange data via Yahoo Finance",
  "previous_close": "9525.00",
  "change_pct": 0.52
}
```

---

### `get_stock_history`

Fetches historical OHLCV data series.

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | ✅ | Stock ticker |
| `start_date` | string | ❌ | Start date `YYYY-MM-DD` |
| `end_date` | string | ❌ | End date `YYYY-MM-DD` |
| `interval` | string | ❌ | Candle interval: `1d`, `1wk`, `1mo` (default: `1d`) |

**Output:** Array of `{ timestamp, open, high, low, close, volume }` records with metadata.

---

### `analyze_stock`

Calculates technical indicators and risk metrics.

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | ✅ | Stock ticker |
| `analysis_period` | string | ❌ | Period: `1y`, `6mo`, `3mo` (default: `1y`) |
| `indicators` | list[string] | ❌ | Specific indicators: `SMA50`, `SMA200`, `RSI14`, `MACD`, `BOLLINGER_BANDS` |

**Output:**
```json
{
  "symbol": "BBCA.JK",
  "latest_price": "9575.00",
  "currency": "IDR",
  "analysis_period": "1y",
  "indicators": {
    "sma_50": 9450.25,
    "sma_200": 9200.00,
    "trend_signal": "Golden Cross (Bullish)",
    "rsi_14": 55.30,
    "rsi_signal": "Neutral Momentum",
    "macd": { "macd_line": 52.3, "signal_line": 48.1, "histogram": 4.2, "momentum": "Bullish" },
    "bollinger_bands": { "upper": 9800.0, "middle": 9500.0, "lower": 9200.0 }
  },
  "risk_and_return_metrics": {
    "period_total_return_pct": 12.5,
    "max_drawdown_pct": -8.3,
    "annualized_volatility_pct": 18.7,
    "52_week_high": 10200.0,
    "52_week_low": 8500.0
  },
  "limitations_and_assumptions": "Analytical metrics are computed from historical data..."
}
```

---

## Cryptocurrency Domain

### `get_crypto_quote`

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | ✅ | Crypto symbol: `BTC`, `ETH`, `SOL`, `BNB`, etc. |
| `quote_currency` | string | ❌ | Quote currency (default: `USD`) |

**Output:**
```json
{
  "symbol": "BTC",
  "current_price": "68500.25",
  "quote_currency": "USD",
  "provider": "coingecko",
  "change_24h_pct": 2.45
}
```

---

### `get_crypto_history`

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | ✅ | Crypto symbol |
| `quote_currency` | string | ❌ | Default `USD` |
| `days` | int | ❌ | Lookback days: 7, 30, 90, 365 (default: 30) |

**Output:** Array of `{ timestamp, price }` data points with provider metadata.

---

### `analyze_crypto`

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | ✅ | Crypto symbol |
| `quote_currency` | string | ❌ | Default `USD` |
| `analysis_period` | string | ❌ | Period: `30d`, `90d`, `365d` (default: `30d`) |

**Output:**
```json
{
  "symbol": "ETH",
  "latest_price": "3650.00",
  "historical_return_pct": 15.2,
  "volatility_metrics": {
    "annualized_volatility_pct": 62.5,
    "max_drawdown_pct": -22.4,
    "period_high": 4100.0,
    "period_low": 3100.0
  },
  "indicators": { "sma_7": 3620.0, "sma_30": 3500.0 }
}
```

---

## Cash Flow Domain

### `record_transaction`

Records a personal income or expense.

**Input:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `transaction_type` | string | ✅ | `income` or `expense` |
| `amount` | float | ✅ | Must be > 0 |
| `category` | string | ✅ | e.g., `Salary`, `Rent`, `Groceries` |
| `transaction_date` | string | ✅ | `YYYY-MM-DD` |
| `currency` | string | ❌ | Default `USD` |
| `description` | string | ❌ | Memo |
| `idempotency_key` | string | ❌ | Client dedup key |

**Output:**
```json
{
  "id": "a1b2c3d4-...",
  "transaction_type": "expense",
  "amount": "250000.00",
  "currency": "IDR",
  "category": "Groceries",
  "persistence_status": "persisted"
}
```

---

### `list_transactions`

**Input:** `start_date`, `end_date`, `transaction_type`, `category`, `limit`, `offset`

**Output:** Paginated list of transactions with `total_count`.

---

### `get_cashflow_report`

**Input:** `start_date`, `end_date`, `currency`, `category_filters`

**Output:**
```json
{
  "total_income": "15000000.00",
  "total_expenses": "8500000.00",
  "net_cash_flow": "6500000.00",
  "income_breakdown_by_category": { "Salary": "12000000.00", "Freelance": "3000000.00" },
  "expense_breakdown_by_category": { "Rent": "3500000.00", "Food": "2500000.00", "Transport": "1500000.00", "Utilities": "1000000.00" },
  "transaction_count": 42,
  "calculation_definitions": { "net_cash_flow": "Total income - Total expenses" }
}
```

---

### `get_expense_breakdown`

**Input:** `start_date`, `end_date`, `currency`, `category_filters`

**Output:** Category spending totals with percentage of total expenses.

---

### `get_monthly_summary`

**Input:** `year`, `month`, `currency`

**Output:** Monthly totals with `comparison_with_previous_month` including `income_change_pct`, `expense_change_pct`, and `net_change_amount`.
