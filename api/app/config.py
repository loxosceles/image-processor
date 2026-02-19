"""Application configuration."""
import os

API_PORT = int(os.getenv("API_PORT", "7432"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "7433"))

CORS_ORIGINS: list[str] = [
    f"http://localhost:{FRONTEND_PORT}",
]