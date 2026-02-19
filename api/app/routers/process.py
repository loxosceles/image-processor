"""Image processing endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/process")
async def process_images() -> dict[str, str]:
    """Process uploaded images (placeholder)."""
    return {"status": "not implemented"}
