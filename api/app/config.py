"""Application configuration."""

import os

# In development, allow all origins. In production, set CORS_ORIGINS env var.
_origins = os.environ.get("CORS_ORIGINS", "")
CORS_ORIGINS: list[str] = _origins.split(",") if _origins else ["*"]
