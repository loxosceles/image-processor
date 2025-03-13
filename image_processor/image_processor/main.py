from typing import Callable, Union
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageFilter
import argparse
from tqdm import tqdm
import piexif

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png"}


def resize_image(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    size: tuple[int, int] = (128, 128),
) -> None:
    """
    Resize an image to the specified size and save it to the output path.

    Args:
        image_path: The path to the input image file.
        output_path: The path to save the resized image.
        size (optional): The desired size for the resized image. Defaults to (128, 128).

    Returns:
        None
    """
    with Image.open(image_path) as img:
        img = img.resize(size)
        img.save(output_path)


def grayscale_image(
    image_path: Union[str, Path], output_path: Union[str, Path]
) -> None:
    """
    Converts an image to grayscale and saves the result.

    Args:
        image_path: The path to the input image file.
        output_path: The path to save the grayscale image.

    Returns:
        None
    """
    with Image.open(image_path) as img:
        img = img.convert("L")
        img.save(output_path)


def blur_image(image_path: Union[str, Path], output_path: Union[str, Path]) -> None:
    """
    Apply a blur filter to an image and save the result.

    Args:
        image_path: The path to the input image file.
        output_path: The path to save the blurred image file.

    Returns:
        None
    """
    with Image.open(image_path) as img:
        img = img.filter(ImageFilter.BLUR)
        img.save(output_path)


def _extract_orientation(img: Image.Image) -> int:
    """
    Extracts the orientation from the EXIF data dictionary.

    Args:
        img: The image object to extract the orientation from.

    Returns:
        int: The orientation value (defaults to 1 if no EXIF data is found).
    """
    exif_data = img.info.get("exif", b"")
    if not exif_data:
        return 1  # Default orientation if no EXIF data is present

    exif_dict = piexif.load(exif_data)
    return exif_dict.get("0th", {}).get(piexif.ImageIFD.Orientation, 1)


def _update_orientation(
    img: Image.Image, orientation: int = 1
) -> tuple[Image.Image, bytes]:
    """
    Updates the orientation tag in the EXIF data dictionary to 1 (normal) or any
    other value, if specified.

    Args:
        img: The image object to update.
        orientation: The orientation value to set. Defaults to 1.
    """
    exif_dict = piexif.load(img.info.get("exif", b""))
    exif_dict["0th"][piexif.ImageIFD.Orientation] = orientation
    exif_bytes = piexif.dump(exif_dict)
    img.info["exif"] = exif_bytes
    return img, exif_bytes


def rotate(image_path: Union[str, Path], output_path: Union[str, Path]) -> None:
    """
    Rotates an image based on its EXIF orientation tag and preserves EXIF
    metadata.

    Args:
        image_path: Path to the input image.
        output_path: Path to save the output image.
    """
    rotated_img = None

    with Image.open(image_path) as img:
        # Extract EXIF data
        orientation = _extract_orientation(img)

        # Apply rotation based on EXIF orientation
        if orientation == 3:
            print(
                f"{image_path}: Orientation is 3. Applying rotation of 180 degrees.")
            rotated_img = img.rotate(180)
        elif orientation == 6:
            print(
                f"{image_path}: Orientation is 6. Applying rotation of 270 degrees.")
            rotated_img = img.rotate(270)
        elif orientation == 8:
            print(f"{image_path}: Orientation is 8. Applying rotation of 90 degrees.")
            rotated_img = img.rotate(90)
        else:
            print(f"{image_path}: No rotation needed (orientation is 1).")

        exif_updated_img, exif_bytes = _update_orientation(
            rotated_img if rotated_img is not None else img
        )

        # Save the rotated image with updated EXIF metadata
        exif_updated_img.save(output_path, exif=exif_bytes)


def process_images(
    image_folder: Union[str, Path],
    output_folder: Union[str, Path],
    process_function: Callable[[Union[str, Path], Union[str, Path]], None],
) -> None:
    """
    Processes images in a given folder using a specified processing function and
    saves the results to an output folder.

    Args:
        image_folder (str or Path): The path to the folder containing the input images.
        output_folder (str or Path): The path to the folder where the processed
            images will be saved.
        process_function (Callable): A function that takes two arguments
            (input_path, output_path) and processes the image.

    Raises:
        Exception: If there is an error processing any of the images, it will be caught and printed.
    """
    output_path = Path(output_folder)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    image_files = [
        f.name
        for f in Path(image_folder).iterdir()
        if f.suffix.lower() in SUPPORTED_SUFFIXES
    ]

    with ThreadPoolExecutor() as executor:
        jobs: list = []
        for image_file in image_files:
            input_path = Path(image_folder) / image_file
            output_path = Path(output_folder) / image_file
            jobs.append(executor.submit(
                process_function, input_path, output_path))

        for job in tqdm(as_completed(jobs), total=len(jobs), desc="Processing Images"):
            try:
                job.result()
            except Exception as e:
                print(f"Error processing image: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concurrent Image Processing")
    parser.add_argument("input_folder", help="Folder containing input images")
    parser.add_argument(
        "output_folder", help="Folder to save processed images")
    parser.add_argument(
        "--task",
        choices=["rotate", "resize", "grayscale", "blur"],
        required=True,
        help="Image processing task",
    )

    args = parser.parse_args()

    task_function = {
        "rotate": rotate,
        "resize": resize_image,
        "grayscale": grayscale_image,
        "blur": blur_image,
    }[args.task]

    process_images(args.input_folder, args.output_folder,
                   task_function)  # type: ignore
