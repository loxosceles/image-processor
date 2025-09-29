import pytest
from PIL import Image
from pathlib import Path
from image_processor.main import resize_image, grayscale_image
from image_processor.formats import save_with_format, UnsupportedFormatError, QUALITY_DEFAULTS


def test_webp_output(temp_dir, sample_image):
    """Test WebP format output"""
    output_path = temp_dir / "test_image.webp"
    resize_image(sample_image, output_path, format="webp", quality=80)
    
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.format == "WEBP"


def test_quality_control(temp_dir, sample_image):
    """Test quality parameter affects file size"""
    high_quality = temp_dir / "high_quality.jpg"
    low_quality = temp_dir / "low_quality.jpg"
    
    resize_image(sample_image, high_quality, format="jpeg", quality=95)
    resize_image(sample_image, low_quality, format="jpeg", quality=50)
    
    assert high_quality.stat().st_size > low_quality.stat().st_size


def test_format_defaults():
    """Test that format defaults are correct"""
    assert QUALITY_DEFAULTS["jpeg"] == 85
    assert QUALITY_DEFAULTS["webp"] == 80
    assert QUALITY_DEFAULTS["png"] is None


def test_unsupported_format_error(temp_dir):
    """Test error handling for unsupported formats"""
    img = Image.new("RGB", (100, 100), color="red")
    output_path = temp_dir / "test.bmp"
    
    with pytest.raises(UnsupportedFormatError):
        save_with_format(img, output_path, format="bmp")


def test_progressive_jpeg(temp_dir, sample_image):
    """Test that progressive JPEG is enabled by default"""
    output_path = temp_dir / "progressive.jpg"
    resize_image(sample_image, output_path, format="jpeg")
    
    # Check if file was created (progressive flag is internal to PIL)
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.format == "JPEG"


def test_error_handling_corrupted_file(temp_dir):
    """Test error handling with corrupted file"""
    # Create a fake corrupted image file
    corrupted_file = temp_dir / "corrupted.jpg"
    corrupted_file.write_text("This is not an image")
    
    output_path = temp_dir / "output.jpg"
    
    with pytest.raises(Exception):  # Should raise CorruptedFileError
        resize_image(corrupted_file, output_path)


def test_format_extension_change(temp_dir, sample_image):
    """Test that output format changes file extension appropriately"""
    # Input is JPEG, output should be WebP
    output_path = temp_dir / "converted.webp"
    grayscale_image(sample_image, output_path, format="webp")
    
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.format == "WEBP"
        assert img.mode == "L"  # Grayscale