"""Tests for /api/process endpoint."""

import zipfile
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient


def test_health(client: TestClient):
    """Health endpoint returns ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_grayscale(client: TestClient, sample_image: Path):
    """Process single image with grayscale task."""
    with open(sample_image, "rb") as f:
        response = client.post(
            "/api/process",
            files={"files": ("test.jpg", f, "image/jpeg")},
            data={"task": "grayscale", "format": "webp"},
        )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert int(response.headers["x-processed-count"]) == 1

    with zipfile.ZipFile(BytesIO(response.content)) as zf:
        assert "test.webp" in zf.namelist()


def test_process_all_tasks(client: TestClient, sample_image: Path):
    """All task types work."""
    for task in ["resize", "grayscale", "blur", "rotate"]:
        with open(sample_image, "rb") as f:
            response = client.post(
                "/api/process",
                files={"files": ("test.jpg", f, "image/jpeg")},
                data={"task": task, "format": "webp"},
            )
        assert response.status_code == 200, f"Task {task} failed"


def test_process_all_formats(client: TestClient, sample_image: Path):
    """All output formats work."""
    for fmt in ["jpeg", "webp", "png"]:
        with open(sample_image, "rb") as f:
            response = client.post(
                "/api/process",
                files={"files": ("test.jpg", f, "image/jpeg")},
                data={"task": "grayscale", "format": fmt},
            )
        assert response.status_code == 200, f"Format {fmt} failed"


def test_invalid_quality_rejected(client: TestClient, sample_image: Path):
    """Quality outside 0-100 is rejected."""
    with open(sample_image, "rb") as f:
        response = client.post(
            "/api/process",
            files={"files": ("test.jpg", f, "image/jpeg")},
            data={"task": "grayscale", "format": "webp", "quality": "150"},
        )
    assert response.status_code == 400


def test_unsupported_file_type_rejected(client: TestClient, tmp_path: Path):
    """Non-image files are rejected."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("not an image")

    with open(txt_file, "rb") as f:
        response = client.post(
            "/api/process",
            files={"files": ("test.txt", f, "text/plain")},
            data={"task": "grayscale", "format": "webp"},
        )
    assert response.status_code == 400
