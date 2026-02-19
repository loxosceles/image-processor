"""Pytest fixtures for API tests."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a minimal valid JPEG for testing."""
    from PIL import Image

    img_path = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path, "JPEG")
    return img_path
