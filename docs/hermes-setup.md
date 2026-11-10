# Hermes MCP Integration Guide

## Overview

Hermes Agent connects to the Financial Agent Tools MCP server via **stdio transport**. The server runs as a local subprocess that Hermes launches and communicates with over stdin/stdout.

## Prerequisites

1. **Hermes Agent** is running with Ollama (`hermes3:8b`)
2. **PostgreSQL** is running via Docker Compose:
   ```bash
   docker compose up -d
   ```
3. **Database migrations** are applied:
   ```bash
   alembic upgrade head
   ```
4. **Dependencies** are installed in a virtual environment:
   ```bash
   source venv/bin/activate
   pip install -e .
   ```

## Hermes MCP Configuration

Add the following to your Hermes MCP configuration file (typically `~/.config/hermes/mcp.json` or equivalent):

```json
{
  "mcpServers": {
    "financial-tools": {
      "command": "/absolute/path/to/financial-agent-tools/venv/bin/python",
      "args": ["-m", "financial_tools.server"],
      "cwd": "/absolute/path/to/financial-agent-tools",
      "env": {
        "PYTHONPATH": "/absolute/path/to/financial-agent-tools/src",
        "DATABASE_URL": "postgresql+psycopg://postgres:postgres@localhost:5432/financial_tools"
      }
    }
  }
}
```

> **Important**: Replace `/absolute/path/to/financial-agent-tools` with the actual absolute path to the project directory.

## Verify Tool Discovery

After configuring and restarting Hermes, the following tools should be available:

**Stock Domain:**
- `get_stock_quote` — current stock price
- `get_stock_history` — historical OHLCV data
- `analyze_stock` — technical indicators and risk metrics

**Crypto Domain:**
- `get_crypto_quote` — current crypto price
- `get_crypto_history` — historical price series
- `analyze_crypto` — returns and volatility metrics

**Cash Flow Domain:**
- `record_transaction` — log income/expense
- `list_transactions` — query transactions
- `get_cashflow_report` — income/expense/net statement
- `get_expense_breakdown` — expense category percentages
- `get_monthly_summary` — monthly totals with comparison

## Smoke Test

Run the check script independently to verify tools load correctly:

```bash
cd /path/to/financial-agent-tools
PYTHONPATH=src python scripts/check_mcp.py
```

Expected output: 11 tools listed with names and descriptions.

## Troubleshooting

### "No tools found" in Hermes

- Ensure the Python path in `command` is the **absolute** path to the venv interpreter.
- Check that `PYTHONPATH` in `env` points to the `src/` directory.
- Restart Hermes after any configuration change.

### Database connection errors

- Verify PostgreSQL is running: `docker compose ps`
- Check the `DATABASE_URL` matches the Docker Compose credentials.
- Ensure migrations are applied: `alembic current`

### Provider timeouts

- Stock/Crypto tools depend on Yahoo Finance and CoinGecko.
- Temporary network issues or rate limits will return clear error messages.
- The system retries transient failures up to 2 times with exponential backoff.

### MCP stdio logs

- All diagnostic logs go to **stderr**, keeping stdout clean for MCP protocol.
- Set `LOG_LEVEL=DEBUG` in `.env` for verbose output.

## Reload / Restart

Changing `server.py`, configuration, or tools requires restarting the MCP server:

1. Close/restart the Hermes session that uses the MCP server.
2. Hermes will re-launch the subprocess on the next session.

Configuration-only changes (`.env`, database URL) take effect on the next server start without code changes.
