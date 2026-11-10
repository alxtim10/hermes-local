oke saya punya proposal yang lebih baik seperti dibawah, sebelum itu ganti nama folder ini menjadi financial-agent-tools

# Project Specification: Modular Financial MCP Infrastructure for Hermes Agent

## 1. Project Overview

Build a modular financial tools infrastructure that integrates with Hermes Agent through the Model Context Protocol (MCP).

The system will provide three independent financial domains:

1. **Stock Analysis Tools** — stock market data retrieval and stock analysis.
2. **Cryptocurrency Tools** — crypto market data retrieval and crypto analysis.
3. **Cash Flow Management Tools** — income and expense tracking, transaction management, and financial reporting.

The primary goal is to allow Hermes Agent to discover and invoke the appropriate financial tools based on natural-language user requests. Hermes acts as the AI orchestrator, while the backend is responsible for deterministic business logic, data access, financial calculations, validation, and security.

Design the infrastructure for local development first, with a clear migration path toward production deployment and independently deployable MCP servers.

## 2. Technology Stack

Use the following technology stack unless a technical incompatibility requires an alternative. Document any proposed changes before implementation.

- Language: Python 3.11+
- MCP integration: Official Python MCP SDK using FastMCP
- Data validation: Pydantic
- Database: PostgreSQL
- ORM: SQLAlchemy 2.x
- Database migrations: Alembic
- HTTP client: httpx
- Configuration: pydantic-settings and environment variables
- Testing: pytest
- Code quality: Ruff and mypy where practical
- Dependency management: pyproject.toml with a reproducible lockfile
- Containerization: Docker and Docker Compose
- Logging: Python standard logging with structured output where appropriate

Use stable, mutually compatible dependency versions. Verify current MCP SDK APIs and Hermes MCP configuration syntax against their official documentation rather than relying on outdated examples.

Do not introduce Redis, Kafka, Kubernetes, microservices, or other infrastructure unless justified by an explicit requirement.

## 3. High-Level Architecture

Implement the following logical architecture:

User Interface
    |
    v
Hermes Agent
    |
    v
MCP Tool Layer
    |
    +-- Stock Domain
    |
    +-- Cryptocurrency Domain
    |
    +-- Cash Flow Domain
    |
    v
Application Services
    |
    +-- Market Data Providers
    +-- Financial Calculation Services
    +-- Transaction Repository
    +-- Reporting Services
    |
    v
PostgreSQL and External Data Providers

Responsibilities:

- Hermes Agent interprets natural-language requests, selects tools, passes arguments, and synthesizes results.
- MCP tools expose clearly defined functions and input/output schemas.
- Application services implement deterministic financial business logic.
- Repositories handle database access.
- Providers integrate with external market data APIs.
- PostgreSQL stores persistent user transactions and any other data that requires persistence.
- Shared infrastructure provides configuration, logging, error handling, database connectivity, and validation.

Keep the business logic independent of the MCP transport layer so that it can be reused by a future REST API, CLI, or web application.

## 4. Repository and Folder Structure

Create the following project structure:

financial-agent-tools/
├── src/
│   └── financial_tools/
│       ├── __init__.py
│       ├── server.py
│       ├── config.py
│       ├── dependencies.py
│       │
│       ├── stocks/
│       │   ├── __init__.py
│       │   ├── tools.py
│       │   ├── service.py
│       │   ├── provider.py
│       │   ├── schemas.py
│       │   └── calculations.py
│       │
│       ├── crypto/
│       │   ├── __init__.py
│       │   ├── tools.py
│       │   ├── service.py
│       │   ├── provider.py
│       │   ├── schemas.py
│       │   └── calculations.py
│       │
│       ├── cashflow/
│       │   ├── __init__.py
│       │   ├── tools.py
│       │   ├── service.py
│       │   ├── repository.py
│       │   ├── schemas.py
│       │   └── reports.py
│       │
│       ├── shared/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── models.py
│       │   ├── exceptions.py
│       │   ├── logging.py
│       │   ├── http_client.py
│       │   ├── security.py
│       │   └── types.py
│       │
│       └── migrations/
│
├── tests/
│   ├── unit/
│   │   ├── test_stocks.py
│   │   ├── test_crypto.py
│   │   └── test_cashflow.py
│   ├── integration/
│   │   ├── test_mcp_tools.py
│   │   └── test_database.py
│   └── conftest.py
│
├── scripts/
│   ├── setup_dev.sh
│   └── check_mcp.py
│
├── docs/
│   ├── architecture.md
│   ├── tool-catalog.md
│   ├── database-schema.md
│   └── hermes-setup.md
│
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── alembic.ini
└── README.md

You may adjust the structure when necessary, but explain significant deviations. Do not create empty files solely to match the tree; implement meaningful functionality in each module.

## 5. Stock Domain

Implement an independent stock analysis module.

Expose the following MCP tools:

### get_stock_quote
Input:
- symbol: string
- optional currency or exchange identifier when supported

Output:
- symbol
- price
- currency
- market timestamp
- data source
- data freshness information

### get_stock_history
Input:
- symbol
- start_date
- end_date
- optional interval

Output:
- historical OHLCV data
- currency
- source
- timestamp and data quality metadata

### analyze_stock
Input:
- symbol
- optional analysis period
- optional list of technical indicators

Output:
- latest available price
- selected technical indicators
- historical return and volatility metrics when sufficient data is available
- analysis period
- data source and timestamp
- limitations and calculation assumptions

Requirements:

- Support Indonesian stock symbols such as BBCA.JK where the chosen provider supports them.
- Separate market data retrieval from calculations.
- Handle missing values, invalid symbols, API errors, rate limits, and stale data.
- Do not fabricate unavailable market prices.
- Distinguish historical observations from forecasts.
- Make clear that technical indicators are analytical metrics, not guarantees of future performance.

## 6. Cryptocurrency Domain

Implement an independent cryptocurrency module.

Expose the following MCP tools:

### get_crypto_quote
Input:
- symbol
- quote currency, defaulting to USD where appropriate

Output:
- symbol
- current price
- quote currency
- market timestamp
- provider
- freshness metadata

### get_crypto_history
Input:
- symbol
- quote currency
- start_date
- end_date
- optional interval

Output:
- historical price series
- timestamp
- provider and data quality metadata

### analyze_crypto
Input:
- symbol
- quote currency
- optional analysis period

Output:
- latest available price
- historical return
- volatility metrics
- optional supported technical indicators
- data source and timestamp
- assumptions and limitations

Requirements:

- Use a provider abstraction to avoid hard-coupling the domain to one API.
- Start with one documented provider and implement a clear extension point for additional providers.
- Normalize symbols and quote currencies consistently.
- Handle missing data, API errors, rate limits, and stale prices.
- Do not confuse realized historical performance with predicted future returns.

## 7. Cash Flow Domain

Implement a persistent personal income and expense management module.

Use PostgreSQL as the authoritative data source for stored transactions.

Expose these MCP tools:

### record_transaction
Input:
- transaction_type: income or expense
- amount
- currency
- category
- transaction_date
- description
- optional account or payment method
- idempotency key when applicable

Output:
- transaction ID
- normalized transaction details
- persistence status

Requirements:
- Validate positive amounts and supported currencies.
- Require a clearly defined user identity or account scope.
- Prevent duplicate writes where idempotency is supported.
- Require explicit confirmation before any consequential write when the host interaction flow calls for it.
- Never silently invent missing transaction details.

### list_transactions
Input:
- start_date
- end_date
- optional transaction_type
- optional category
- pagination parameters

Output:
- matching transactions
- pagination metadata
- requested period

### get_cashflow_report
Input:
- start_date
- end_date
- currency
- optional category filters

Output:
- total income
- total expenses
- net cash flow
- income breakdown by category
- expense breakdown by category
- transaction count
- reporting period
- currency
- calculation definitions

Use the following definition:

Net cash flow = Total income - Total expenses

Do not mix asset market value changes with cash income or expenses unless a future feature explicitly defines that accounting treatment.

### get_expense_breakdown
Input:
- start_date
- end_date
- optional category filters
- currency

Output:
- spending by category
- percentage of total expenses
- total expenses
- reporting period

### get_monthly_summary
Input:
- year
- month
- currency

Output:
- total income
- total expenses
- net cash flow
- comparison with the previous month when comparable data exists

Requirements:

- Use database transactions for writes.
- Use parameterized queries and ORM-safe database access.
- Store timestamps and transaction dates consistently.
- Define how timezone and currency conversion are handled.
- Use decimal-safe monetary representations; do not use binary floating-point arithmetic for authoritative monetary calculations.
- Distinguish zero activity from unavailable data.
- Ensure every query is scoped to the correct user.
- Support categories through a consistent validation strategy.
- Include database migrations and indexes for frequent date-range queries.

## 8. Database Design

Create an initial normalized PostgreSQL schema.

At minimum, define:

### users
- id
- external_user_id or stable application identity
- created_at
- updated_at

### transactions
- id
- user_id
- transaction_type
- amount
- currency
- category
- description
- transaction_date
- created_at
- updated_at
- idempotency_key where applicable

Define appropriate foreign keys, unique constraints, indexes, and check constraints.

Requirements:

- Use UUIDs or another consistent primary key strategy.
- Store monetary amounts with an appropriate NUMERIC/DECIMAL precision.
- Index user_id and transaction_date for report queries.
- Add indexes and uniqueness constraints where justified.
- Never assume a single global user when deploying an application that may serve multiple users.
- Avoid storing provider API secrets in the database unless there is an explicit secure credential-management design.

Historical market data may remain provider-sourced initially. Do not duplicate large market data sets in PostgreSQL unless caching, reproducibility, or offline analysis requires it.

Provide an initial Alembic migration and document how to apply and roll back migrations.

## 9. Shared Infrastructure

Implement the following components:

### Configuration
- Load configuration from environment variables.
- Validate required settings at startup.
- Provide safe defaults for local development.
- Never commit secrets.

### Database
- Configure SQLAlchemy sessions and engine lifecycle.
- Provide safe transaction management.
- Handle connection failures.
- Support test database configuration.

### HTTP client
- Configure timeouts.
- Support bounded retries for appropriate transient errors.
- Handle HTTP status errors and provider rate limits.
- Avoid retrying non-idempotent writes blindly.

### Error handling
Define consistent internal exceptions for:
- Invalid input
- Resource not found
- Provider unavailable
- Rate limit exceeded
- Stale data
- Database failure
- Unauthorized access
- Duplicate transaction

Return clear, sanitized error responses through MCP without exposing secrets, SQL statements, credentials, or internal stack traces.

### Logging
- Use structured logs where appropriate.
- Include tool name, request correlation ID, duration, and result status.
- Never log API keys, passwords, or unnecessary sensitive financial details.
- Keep standard output clean when using MCP stdio transport; send diagnostics to standard error or an appropriate logging destination.

## 10. MCP Server Implementation

Implement a single MCP server initially.

Requirements:

- Use the official Python MCP SDK and supported FastMCP APIs.
- Register stock, crypto, and cash flow tools through separate domain registration functions.
- Keep tool descriptions explicit, concise, and useful for LLM tool selection.
- Use typed parameters and validated outputs.
- Return structured results whenever supported.
- Separate the transport layer from application services.
- Support stdio transport for local Hermes integration.
- Ensure the server can start using a documented Python module command.
- Provide a tool inventory that lists tool names, purposes, input schemas, and output schemas.

Do not make the model responsible for executing raw SQL, computing authoritative account balances, or bypassing domain validation.

## 11. Hermes Integration

Provide a working example of Hermes configuration for the MCP server.

Requirements:

- Verify the current Hermes configuration schema and supported MCP transport options from official documentation.
- Use absolute paths for the Python interpreter or a clearly documented alternative.
- Configure environment variables securely.
- Document the steps to register, start, inspect, enable, disable, and troubleshoot the MCP server.
- Explain how the exposed tools are named and discovered.
- Provide a minimal smoke test that confirms the expected tools are available.
- Document how to verify that Hermes invokes the correct tool for a sample user request.

Do not assume that changing a configuration automatically refreshes every active Hermes session. Document the appropriate reload or restart procedure based on the installed version.

## 12. Security and Financial Data Integrity

Treat all financial data and external provider responses as untrusted input.

Implement:

- Input validation at tool boundaries.
- User-level authorization for private financial records.
- Least-privilege database access.
- Secret management through environment variables or a suitable secrets manager.
- SQL injection prevention.
- Safe external HTTP handling.
- No arbitrary shell execution or unrestricted SQL tools.
- Explicit handling of consequential financial write operations.
- Audit-friendly records for transaction changes where appropriate.

Market-data analysis tools should be read-only in the initial implementation.

Do not implement real-money trading, brokerage order execution, or automatic transfers in this phase.

## 13. Testing Strategy

Implement meaningful tests for:

### Unit tests
- Technical indicator calculations.
- Historical return and volatility calculations.
- Cash flow totals.
- Expense category percentages.
- Input validation.
- Currency handling.
- Error mapping.

### Integration tests
- MCP tool registration and invocation.
- PostgreSQL repository operations.
- Alembic migrations.
- Provider response normalization.

### Edge cases
- Empty reporting periods.
- Invalid date ranges.
- Invalid symbols.
- Missing provider data.
- Stale market data.
- Rate limits.
- Duplicate transactions.
- Unauthorized user access.
- Database connection failure.
- Currency mismatch.
- Zero expense totals.

Use mocked market data providers in normal automated tests. Tests must not require paid APIs or real financial credentials.

## 14. Local Development and Deployment

Provide a Docker Compose setup for PostgreSQL and the application where appropriate.

Requirements:

- Include a PostgreSQL health check.
- Use a persistent development database volume.
- Add a non-root application user in the production-oriented container image.
- Separate local development configuration from production configuration.
- Do not expose the database publicly by default.
- Provide database initialization and migration commands.
- Document backup and restore considerations.
- Do not put secrets in Docker images or committed Compose files.

Since Hermes launches a local stdio MCP server, explain how to run it in the same environment as Hermes. If Hermes runs on the host and PostgreSQL runs in Docker, document the appropriate connection settings.

Keep the first deployment simple. Do not add Kubernetes or distributed infrastructure unless explicitly requested.

## 15. Documentation Deliverables

Generate:

- README.md with setup and usage instructions.
- docs/architecture.md with architecture decisions and data flow.
- docs/tool-catalog.md with every MCP tool and its schema.
- docs/database-schema.md with entities, relationships, and migrations.
- docs/hermes-setup.md with Hermes configuration and troubleshooting.
- .env.example with placeholder values only.
- Example MCP tool invocations and representative output.
- Commands for installing dependencies, running tests, applying migrations, and starting the server.

Include Mermaid diagrams for component architecture and transaction/reporting flows where useful.

## 16. Implementation Workflow

Work incrementally instead of generating the entire codebase in one unverified pass.

Phase 1: Inspect the repository and summarize the intended architecture.

Phase 2: Create the Python package, dependency configuration, settings, logging, shared exceptions, and database infrastructure.

Phase 3: Implement the cash flow domain and PostgreSQL migrations.

Phase 4: Implement stock and cryptocurrency provider abstractions and calculations.

Phase 5: Register and test all MCP tools.

Phase 6: Configure and test Hermes integration.

Phase 7: Add Docker Compose, documentation, security checks, and final validation.

After each phase:
- List the files created or modified.
- Explain significant implementation decisions.
- Run relevant tests and static checks.
- Fix failures before continuing.
- Report unresolved issues explicitly.

Before modifying an existing repository, inspect its files and preserve useful existing code. Do not overwrite existing user work without a clear reason.

Do not claim that integrations or tests work unless they have actually been verified.

## 17. Definition of Done

The project is considered complete when:

1. The Python package installs successfully.
2. PostgreSQL starts and passes its health check.
3. Database migrations can be applied successfully.
4. Cash flow transactions can be created and queried in an isolated test environment.
5. Cash flow reports return correct deterministic totals.
6. Stock and crypto providers return validated data or clear provider errors.
7. All MCP tools are discoverable through the running server.
8. Hermes can invoke the appropriate tools using the documented configuration.
9. Automated tests pass.
10. Secrets are excluded from version control.
11. Documentation is sufficient for another developer to reproduce the setup.
12. The system clearly distinguishes real provider data, stored financial records, calculations, and unavailable information.

Start by inspecting the current repository, presenting the architecture and implementation plan, and then proceed with Phase 1. Do not stop after generating documentation or placeholder files; implement and verify each phase.
