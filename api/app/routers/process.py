"""Image processing endpoint."""

import io
import tempfile
import zipfile
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from image_processor.formats import (
    QUALITY_DEFAULTS,
    CorruptedFileError,
    UnsupportedFormatError,
)
from image_processor.main import (
    SUPPORTED_SUFFIXES,
    blur_image,
    grayscale_image,
    resize_image,
    rotate,
)

router = APIRouter()

TASK_FUNCTIONS = {
    "resize": resize_image,
    "grayscale": grayscale_image,
    "blur": blur_image,
    "rotate": rotate,
}


def _validate_file(file: UploadFile) -> None:
    """Validate uploaded file has supported extension."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="File must have a filename")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}",
        )


@router.post("/process")
async def process_images(
    files: list[UploadFile] = File(...),
    task: Literal["resize", "grayscale", "blur", "rotate"] = Form(...),
    format: Literal["jpeg", "webp", "png"] = Form("webp"),
    quality: int | None = Form(None),
    size: int = Form(128),
    aspect_ratio: str = Form("original"),
) -> StreamingResponse:
    """Process uploaded images with specified task and format."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    if quality is not None and not 0 <= quality <= 100:
        raise HTTPException(status_code=400, detail="Quality must be between 0 and 100")

    if quality is None:
        quality = QUALITY_DEFAULTS.get(format, 85)

    for file in files:
        _validate_file(file)

    process_fn = TASK_FUNCTIONS[task]
    zip_buffer = io.BytesIO()
    errors: list[str] = []
    processed_count = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                try:
                    input_path = tmppath / file.filename
                    content = await file.read()
                    input_path.write_bytes(content)

                    output_name = f"{input_path.stem}.{format}"
                    output_path = tmppath / output_name

                    if task == "resize":
                        process_fn(
                            input_path, output_path, format, quality,
                            (size, size), aspect_ratio
                        )
                    else:
                        process_fn(input_path, output_path, format, quality)

                    zf.write(output_path, output_name)
                    processed_count += 1

                except (CorruptedFileError, UnsupportedFormatError) as err:
                    errors.append(f"{file.filename}: {err}")
                except Exception as err:
                    errors.append(f"{file.filename}: {err}")

    if processed_count == 0:
        raise HTTPException(
            status_code=422,
            detail=f"All files failed: {'; '.join(errors[:5])}",
        )

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=processed.zip",
            "X-Processed-Count": str(processed_count),
            "X-Error-Count": str(len(errors)),
        },
    )
