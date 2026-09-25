"""Application configuration loaded from environment variables.

Supports a .env file at the project root for local development.
"""

import os
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Loaded from environment variables with .env file support.
    """

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ------------------------------------------------------------------
    # Output mode for MCP render tools
    #   "inline" – return the full data (base64 / svg / html) in the response
    #   "url"    – save to disk and return only a URL to the file
    # ------------------------------------------------------------------
    MCP_OUTPUT_MODE: Literal["inline", "url"] = "url"

    # ------------------------------------------------------------------
    # Static / output file storage
    # ------------------------------------------------------------------
    OUTPUT_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "output")
    STATIC_URL_PREFIX: str = "/static"

    # ------------------------------------------------------------------
    # Base URL used to build absolute file URLs when MCP_OUTPUT_MODE=url
    # In production this should be the public-facing host, e.g.
    #   https://viz.example.com
    # ------------------------------------------------------------------
    BASE_URL: str = "http://localhost:8000"


# Singleton
settings = Settings()