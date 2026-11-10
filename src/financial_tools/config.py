"""Application configuration management via pydantic-settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = Field(default="development", description="App environment")
    log_level: str = Field(default="INFO", description="Logging level")

    # Provider configurations
    crypto_api_base_url: str = Field(
        default="https://api.coingecko.com/api/v3",
        description="CoinGecko API base URL",
    )
    crypto_api_timeout_seconds: float = Field(
        default=15.0,
        description="Timeout for crypto API requests",
    )
    stock_api_timeout_seconds: float = Field(
        default=15.0,
        description="Timeout for stock data requests",
    )


settings = Settings()
