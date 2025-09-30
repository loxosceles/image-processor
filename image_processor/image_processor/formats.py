from typing import Union, Optional
from pathlib import Path
from PIL import Image


class ImageProcessingError(Exception):
    """Base exception for image processing errors"""
    pass


class UnsupportedFormatError(ImageProcessingError):
    """Raised when an unsupported format is requested"""
    pass


class CorruptedFileError(ImageProcessingError):
    """Raised when a file cannot be processed due to corruption"""
    pass


SUPPORTED_FORMATS = {"jpeg", "jpg", "webp", "png"}
QUALITY_DEFAULTS = {"jpeg": 85, "webp": 80, "png": None}


def save_with_format(
    img: Image.Image,
    output_path: Union[str, Path],
    format: str = "jpeg",
    quality: Optional[int] = None,
    progressive: bool = True
) -> None:
    """Save image with specified format and quality settings"""
    format = format.lower()
    if format not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(
            f"Format '{format}' not supported. Use: {', '.join(SUPPORTED_FORMATS)}")

    if quality is None:
        quality = QUALITY_DEFAULTS.get(format, 85)

    save_kwargs = {}

    if format in ["jpeg", "jpg"]:
        save_kwargs.update({
            "format": "JPEG",
            "quality": quality,
            "progressive": progressive,
            "optimize": True
        })
    elif format == "webp":
        save_kwargs.update({
            "format": "WEBP",
            "quality": quality,
            "optimize": True
        })
    elif format == "png":
        save_kwargs.update({
            "format": "PNG",
            "optimize": True
        })

    try:
        img.save(output_path, **save_kwargs)
    except Exception as e:
        raise ImageProcessingError(f"Failed to save {output_path}: {e}")
