FROM python:3.11-slim AS builder

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/

RUN pip install --no-cache-dir .

COPY scripts/ ./scripts/
COPY alembic.ini ./

USER appuser

CMD ["python", "-m", "financial_tools.server"]
