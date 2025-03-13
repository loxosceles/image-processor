import pytest
from PIL import Image, ImageFilter
import io
from image_processor.main import (
    resize_image,
    grayscale_image,
    blur_image,
    rotate,
    process_images,
    _extract_orientation,
    _update_orientation,
    SUPPORTED_SUFFIXES,
)
import piexif


def test_extract_orientation(sample_image, image_rotated_by_270):
    """
    Test that _extract_orientation correctly extracts the orientation from EXIF data.
    """
    # Image without EXIF orientation
    orientation = _extract_orientation(Image.open(sample_image))
    assert orientation == 1  # Default orientation is 1 (normal)

    # Image with EXIF data and orientation 8 (270°)
    orientation = _extract_orientation(Image.open(image_rotated_by_270))
    assert orientation == 8  # Expected orientation is 8 (270°)


def test_update_orientation(image_with_orientation):
    """
    Test that _update_orientation correctly updates the orientation in EXIF data.
    """
    # Update orientation to 3 (180°)
    _, exif_bytes = _update_orientation(image_with_orientation, 3)
    exif_dict = piexif.load(exif_bytes)
    assert exif_dict["0th"][piexif.ImageIFD.Orientation] == 3

    # Update orientation to 1 (normal)
    _, exif_bytes = _update_orientation(image_with_orientation, 1)
    exif_dict = piexif.load(exif_bytes)
    assert exif_dict["0th"][piexif.ImageIFD.Orientation] == 1


def test_resize_image(temp_dir, sample_image):
    """Test resize_image function"""
    output_path = temp_dir / "resized_image.jpg"
    resize_image(sample_image, output_path, size=(128, 128))

    # Verify the output image exists and has the correct size
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size == (128, 128)


def test_grayscale_image(temp_dir, sample_image):
    """Test grayscale_image function"""
    output_path = temp_dir / "grayscale_image.jpg"
    grayscale_image(sample_image, output_path)

    # Verify the output image exists and is grayscale
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.mode == "L"  # Grayscale mode


def test_blur_image(temp_dir, sample_image):
    """Test blur_image function"""
    output_path = temp_dir / "blurred_image.jpg"
    blur_image(sample_image, output_path)

    # Verify the output image exists
    assert output_path.exists()
    with Image.open(output_path) as img:
        # Check if the image is blurred (this is a basic check)
        assert img.filter(ImageFilter.BLUR) is not None


# Parametrized test for image rotation
@pytest.mark.parametrize(
    "image_fixture, initial_orientation",
    [
        ("image_rotated_by_90", 6),  # Initial orientation 6 (90°)
        ("image_rotated_by_180", 3),  # Initial orientation 3 (180°)
        ("image_rotated_by_270", 8),  # Initial orientation 8 (270°)
    ],
)
def test_rotate_image(tmp_path, image_fixture, initial_orientation, request):
    """
    Test that the rotate function corrects the orientation of the image.
    """
    # Get the fixture dynamically using request.getfixturevalue
    image_bytes = request.getfixturevalue(image_fixture)

    # Save the rotated image to a temporary file
    input_path = tmp_path / "input_image.jpg"
    output_path = tmp_path / "output_image.jpg"
    with open(input_path, "wb") as f:
        f.write(image_bytes.getvalue())

    # Verify the initial orientation
    with Image.open(input_path) as img:
        exif_dict = piexif.load(img.info.get("exif", b""))
        assert exif_dict["0th"][piexif.ImageIFD.Orientation] == initial_orientation

    # Run the rotate function
    rotate(str(input_path), str(output_path))

    # Step 4: Verify the final orientation
    with Image.open(output_path) as img:
        exif_dict = piexif.load(img.info.get("exif", b""))
        # Corrected to normal orientation
        assert exif_dict["0th"][piexif.ImageIFD.Orientation] == 1


def test_process_images(temp_dir):
    """Test process_images function"""
    # Create a second sample image
    sample_image2 = temp_dir / "test_image2.jpg"
    img = Image.new("RGB", (256, 256), color="blue")
    img.save(sample_image2)

    # Create a subdirectory for output
    output_dir = temp_dir / "output"
    output_dir.mkdir()

    # Process images
    process_images(temp_dir, output_dir, resize_image)

    # Verify the output images exist and have the correct size
    for image_file in temp_dir.iterdir():
        if image_file.suffix.lower() in SUPPORTED_SUFFIXES:
            output_path = output_dir / image_file.name
            assert output_path.exists()
            with Image.open(output_path) as img:
                assert img.size == (128, 128)  # Default size for resize_image


def test_unsupported_format(temp_dir):
    """Test unsupported file format"""
    # Create an unsupported file
    unsupported_file = temp_dir / "test_file.txt"
    unsupported_file.write_text("This is not an image.")

    # Create a subdirectory for output
    output_dir = temp_dir / "output"
    output_dir.mkdir()

    # Process images (should ignore the unsupported file)
    process_images(temp_dir, output_dir, resize_image)

    # Verify no output image was created for the unsupported file
    assert not (output_dir / "test_file.txt").exists()


def test_error_handling(temp_dir, monkeypatch):
    """Test error handling in process_images"""
    # Monkeypatch the resize_image function to raise an exception
    def faulty_resize(*args, **kwargs):
        raise ValueError("Test error")

    monkeypatch.setattr("image_processor.main.resize_image", faulty_resize)

    # Create a subdirectory for output
    output_dir = temp_dir / "output"
    output_dir.mkdir()

    # Process images (should catch the error and continue)
    process_images(temp_dir, output_dir, resize_image)

    # Verify the output directory is empty (no images processed due to error)
    assert len(list(output_dir.iterdir())) == 0
