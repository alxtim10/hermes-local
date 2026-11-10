# Architecture

## System Overview

Financial Agent Tools is a modular MCP (Model Context Protocol) infrastructure providing Hermes Agent with deterministic financial tools across three independent domains.

```mermaid
flowchart TD
    User["User (Natural Language)"]
    Hermes["Hermes Agent<br/>hermes3:8b via Ollama"]
    MCP["MCP Server<br/>stdio transport"]

    User --> Hermes
    Hermes <--> MCP

    subgraph Domains
        Stock["Stock Domain<br/>get_stock_quote<br/>get_stock_history<br/>analyze_stock"]
        Crypto["Crypto Domain<br/>get_crypto_quote<br/>get_crypto_history<br/>analyze_crypto"]
        Cash["Cash Flow Domain<br/>record_transaction<br/>list_transactions<br/>get_cashflow_report<br/>get_expense_breakdown<br/>get_monthly_summary"]
    end

    MCP --> Stock
    MCP --> Crypto
    MCP --> Cash

    subgraph Services
        YF["Yahoo Finance<br/>Provider"]
        CG["CoinGecko<br/>Provider"]
        PG["PostgreSQL<br/>Database"]
    end

    Stock --> YF
    Crypto --> CG
    Crypto -.->|fallback| YF
    Cash --> PG
```

## Layered Architecture

Each domain follows a consistent internal layering:

```
tools.py      ← MCP tool registration (transport boundary)
service.py    ← Business logic orchestration
provider.py   ← External data source abstraction (Stock/Crypto only)
calculations.py ← Pure calculation functions
repository.py ← Database access (Cash Flow only)
schemas.py    ← Pydantic input/output models
```

### Design Decisions

1. **Business logic is transport-independent**: Services and calculations have no dependency on MCP. They can be reused by a REST API, CLI, or web app.

2. **Provider abstraction**: Stock and Crypto domains use an abstract base class (`StockDataProvider`, `CryptoDataProvider`) with concrete implementations. Mock providers are included for deterministic testing.

3. **Hybrid Crypto Provider**: The `HybridCryptoProvider` attempts CoinGecko first and falls back to Yahoo Finance, providing resilience without requiring API keys.

4. **Decimal arithmetic**: All monetary calculations use Python `Decimal` — never `float` — to prevent rounding errors in financial reports.

5. **Single MCP server**: All three domains register tools on one `MCPServer` instance. This simplifies local development while the architecture supports splitting into independent servers later.

6. **SQLite fallback**: For local development without PostgreSQL, the database URL can be set to `sqlite:///./financial_tools.db`. Tests always use in-memory SQLite.

## Data Flow: Cash Flow Report

```mermaid
sequenceDiagram
    participant U as User
    participant H as Hermes Agent
    participant M as MCP Server
    participant S as CashflowService
    participant R as Repository
    participant DB as PostgreSQL

    U->>H: "Show my October expenses by category"
    H->>M: get_expense_breakdown(start_date, end_date, currency)
    M->>S: get_expense_breakdown(...)
    S->>R: get_range(user_id, start, end, currency)
    R->>DB: SELECT ... WHERE user_id=? AND date BETWEEN ? AND ?
    DB-->>R: [Transaction rows]
    R-->>S: List[Transaction]
    S->>S: generate_expense_breakdown() with Decimal math
    S-->>M: ExpenseBreakdownResponse
    M-->>H: JSON result
    H-->>U: Natural language summary with category percentages
```

## Data Flow: Stock Analysis

```mermaid
sequenceDiagram
    participant U as User
    participant H as Hermes Agent
    participant M as MCP Server
    participant S as StockService
    participant P as YahooFinanceProvider
    participant C as Calculations

    U->>H: "Analyze BBCA.JK technical indicators for 1 year"
    H->>M: analyze_stock(symbol="BBCA.JK", analysis_period="1y")
    M->>S: analyze_stock(...)
    S->>P: get_history(symbol, period="1y")
    P-->>S: StockHistoryResponse (OHLCV data)
    S->>C: calculate_indicators(data, indicators)
    C-->>S: {sma_50, sma_200, rsi_14, macd, ...}
    S->>C: calculate_risk_metrics(data)
    C-->>S: {max_drawdown, volatility, ...}
    S-->>M: StockAnalysisResponse
    M-->>H: JSON result
    H-->>U: Technical analysis summary with interpretation
```
