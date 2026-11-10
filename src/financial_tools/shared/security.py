"""Security, sanitization, and authorization helpers."""

import re
import uuid
from typing import Optional
from financial_tools.shared.exceptions import InvalidInputError

SYMBOL_PATTERN = re.compile(r"^[A-Za-z0-9\.\-\_\^\=]{1,20}$")
CURRENCY_PATTERN = re.compile(r"^[A-Za-z]{3,5}$")


def validate_symbol(symbol: str) -> str:
    """Validates and normalizes market symbol (stock or crypto)."""
    cleaned = symbol.strip().upper()
    if not cleaned or not SYMBOL_PATTERN.match(cleaned):
        raise InvalidInputError(
            f"Invalid ticker or symbol format: '{symbol}'. Must be 1-20 alphanumeric characters."
        )
    return cleaned


def validate_currency(currency: str) -> str:
    """Validates and normalizes standard ISO or crypto currency code."""
    cleaned = currency.strip().upper()
    if not cleaned or not CURRENCY_PATTERN.match(cleaned):
        raise InvalidInputError(
            f"Invalid currency code: '{currency}'. Must be 3-5 alphabetical characters (e.g., USD, IDR, EUR, BTC)."
        )
    return cleaned


def validate_uuid(user_id_str: str) -> uuid.UUID:
    """Validates and parses string as UUID."""
    try:
        return uuid.UUID(user_id_str)
    except (ValueError, AttributeError):
        raise InvalidInputError(f"Invalid UUID identifier: '{user_id_str}'")


def sanitize_description(description: Optional[str], max_length: int = 500) -> str:
    """Strips leading/trailing whitespace and truncates description to safe length."""
    if not description:
        return ""
    cleaned = description.strip()
    return cleaned[:max_length]
