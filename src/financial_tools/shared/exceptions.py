"""Domain-specific exceptions for Financial Tools."""

from typing import Any, Dict, Optional


class FinancialToolsError(Exception):
    """Base exception for all financial tools domain errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Sanitized representation suitable for MCP error reporting."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
        }


class InvalidInputError(FinancialToolsError):
    """Raised when parameters fail domain validation rules."""
    pass


class ResourceNotFoundError(FinancialToolsError):
    """Raised when a requested resource (e.g., transaction or user) is not found."""
    pass


class ProviderUnavailableError(FinancialToolsError):
    """Raised when an external market provider (e.g. Yahoo Finance, CoinGecko) cannot be reached."""
    pass


class RateLimitExceededError(FinancialToolsError):
    """Raised when external provider or internal rate limits are exceeded."""
    pass


class StaleDataError(FinancialToolsError):
    """Raised when retrieved market data is older than the acceptable freshness window."""
    pass


class DatabaseError(FinancialToolsError):
    """Raised when an internal database operation fails, hiding raw SQL details."""
    pass


class UnauthorizedAccessError(FinancialToolsError):
    """Raised when access to a user-scoped resource is unauthorized."""
    pass


class DuplicateTransactionError(FinancialToolsError):
    """Raised when a transaction write violates idempotency or uniqueness."""
    pass
