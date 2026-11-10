# Financial Agent Tools

Modular Financial MCP Infrastructure for Hermes Agent — providing stock analysis and cryptocurrency tracking through the Model Context Protocol.

## Quick Start

### 1. Prerequisites

- Python 3.11+
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

### 3. Verify MCP Tools

```bash
python scripts/check_mcp.py
```

You should see all 6 tools registered across two domains.

### 4. Start the MCP Server

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
│   └── shared/             # Logging, exceptions, security, http client
├── tests/
│   ├── unit/               # Deterministic unit tests
│   └── conftest.py         # Fixtures (mock providers)
├── scripts/
│   └── check_mcp.py        # Tool discovery inspector
├── docs/                   # Architecture and reference docs
├── pyproject.toml          # Python project metadata
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

Tests use mock providers — no external APIs required.

---

## Documentation

- [Architecture](docs/architecture.md) — system design, data flow, and decisions
- [Tool Catalog](docs/tool-catalog.md) — complete MCP tool schemas and examples
- [Database Schema](docs/database-schema.md) — entities, relationships, and migrations
- [Hermes Setup](docs/hermes-setup.md) — Hermes MCP configuration guide

---

## License

This project is for educational and portfolio purposes.
