# Financial Agent Tools

Modular Financial MCP Infrastructure for Hermes Agent — providing stock analysis, cryptocurrency tracking, and cash flow management through the Model Context Protocol.

## Quick Start

### 1. Prerequisites

- Python 3.11+
- Docker & Docker Compose (for PostgreSQL)
- Ollama with Hermes 3 model (for agent interaction)

### 2. Setup

```bash
# Clone and enter the project
cd financial-agent-tools

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package in development mode
pip install -e ".[dev]"

# Copy environment config
cp .env.example .env
```

### 3. Start PostgreSQL

```bash
docker compose up -d
```

Wait for the health check to pass:

```bash
docker compose ps   # STATUS should show "healthy"
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Verify MCP Tools

```bash
python scripts/check_mcp.py
```

You should see all 11 tools registered across three domains.

### 6. Start the MCP Server

```bash
python -m financial_tools.server
```

The server starts on stdio transport, ready for Hermes integration.

---

## MCP Tool Inventory

| # | Domain | Tool Name | Description |
|---|--------|-----------|-------------|
| 1 | Stock | `get_stock_quote` | Current market price for a stock symbol (e.g., BBCA.JK, AAPL) |
| 2 | Stock | `get_stock_history` | Historical OHLCV data series |
| 3 | Stock | `analyze_stock` | Technical indicators (SMA, RSI, MACD, Bollinger) and risk metrics |
| 4 | Crypto | `get_crypto_quote` | Current crypto price (BTC, ETH, SOL, etc.) |
| 5 | Crypto | `get_crypto_history` | Historical price series |
| 6 | Crypto | `analyze_crypto` | Returns, volatility, and moving averages |
| 7 | Cash Flow | `record_transaction` | Record income or expense with idempotency support |
| 8 | Cash Flow | `list_transactions` | Paginated, filtered transaction listing |
| 9 | Cash Flow | `get_cashflow_report` | Full income/expense/net statement with category breakdowns |
| 10 | Cash Flow | `get_expense_breakdown` | Category-wise expense percentages |
| 11 | Cash Flow | `get_monthly_summary` | Monthly totals with month-over-month comparison |

---

## Project Structure

```
financial-agent-tools/
├── src/financial_tools/
│   ├── server.py           # MCP server entry point
│   ├── config.py           # Settings (pydantic-settings)
│   ├── dependencies.py     # Composition root
│   ├── stocks/             # Stock analysis domain
│   ├── crypto/             # Cryptocurrency domain
│   ├── cashflow/           # Cash flow management domain
│   ├── shared/             # Database, logging, exceptions, security
│   └── migrations/         # Alembic migrations
├── tests/
│   ├── unit/               # Deterministic unit tests
│   └── conftest.py         # Fixtures (in-memory SQLite)
├── scripts/
│   └── check_mcp.py        # Tool discovery inspector
├── docs/                   # Architecture and reference docs
├── compose.yaml            # PostgreSQL container
├── pyproject.toml          # Python project metadata
├── alembic.ini             # Migration configuration
└── .env.example            # Environment template
```

---

## Testing

```bash
# Run all unit tests
PYTHONPATH=src pytest tests/unit/ -v

# Run specific domain
PYTHONPATH=src pytest tests/unit/test_stocks.py -v
```

Tests use mock providers and in-memory SQLite — no external APIs or PostgreSQL required.

---

## Documentation

- [Architecture](docs/architecture.md) — system design, data flow, and decisions
- [Tool Catalog](docs/tool-catalog.md) — complete MCP tool schemas and examples
- [Database Schema](docs/database-schema.md) — entities, relationships, and migrations
- [Hermes Setup](docs/hermes-setup.md) — Hermes MCP configuration guide

---

## License

This project is for educational and portfolio purposes.
