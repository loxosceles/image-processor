import pytest
import io
from PIL import Image
import piexif


@pytest.fixture(scope="function")
def temp_dir(tmp_path):
    """Fixture to create a temporary directory for testing"""
    return tmp_path


@pytest.fixture(scope="function")
def image_without_exif():
    """Fixture to create a sample image without EXIF data."""
    img = Image.new("RGB", (256, 256), color="blue")
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    return Image.open(image_bytes)


@pytest.fixture(scope="function")
def image_with_orientation():
    """Fixture to create a sample image with EXIF orientation."""
    img = Image.new("RGB", (256, 256), color="red")
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Orientation: 6  # Rotate 90 degrees
        },
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    exif_bytes = piexif.dump(exif_dict)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG", exif=exif_bytes)
    image_bytes.seek(0)
    return Image.open(image_bytes)


@pytest.fixture(scope="function")
def sample_image():
    """Fixture to create a sample image for testing"""
    img = Image.new("RGB", (256, 256), color="red")
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    return image_bytes


@pytest.fixture(scope="function")
def image_rotated_by_90():
    """Fixture to create a sample image"""
    img = Image.new("RGB", (256, 256), color="red")
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Orientation: 6  # Rotate 90 degrees
        },
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    exif_bytes = piexif.dump(exif_dict)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG", exif=exif_bytes)
    image_bytes.seek(0)
    return image_bytes


@pytest.fixture(scope="function")
def image_rotated_by_180():
    """Fixture to create a sample image"""
    img = Image.new("RGB", (256, 256), color="red")
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Orientation: 3  # Rotate 180 degrees
        },
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    exif_bytes = piexif.dump(exif_dict)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG", exif=exif_bytes)
    image_bytes.seek(0)
    return image_bytes


@pytest.fixture(scope="function")
def image_rotated_by_270():
    """Fixture to create a sample image"""
    img = Image.new("RGB", (256, 256), color="red")
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Orientation: 8  # Rotate 270 degrees
        },
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    exif_bytes = piexif.dump(exif_dict)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="JPEG", exif=exif_bytes)
    image_bytes.seek(0)
    return image_bytes
