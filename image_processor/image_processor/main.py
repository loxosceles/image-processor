from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Optional, Union

import piexif
from PIL import Image, ImageFilter
from rich.console import Console
from rich.progress import Progress

from .formats import CorruptedFileError, save_with_format

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def resize_image(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    format: str = "jpeg",
    quality: Optional[int] = None,
    size: tuple[int, int] = (128, 128),
) -> None:
    """
    Resize an image to the specified size and save it to the output path.

    Args:
        image_path: The path to the input image file.
        output_path: The path to save the resized image.
        format (optional): Output format. Defaults to "jpeg".
        quality (optional): Compression quality 0-100. Uses format defaults if None.
        size (optional): The desired size for the resized image. Defaults to (128, 128).

    Returns:
        None
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(size)
            save_with_format(img, output_path, format, quality)
    except Exception as e:
        raise CorruptedFileError(f"Failed to process {image_path}: {e}")


def grayscale_image(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    format: str = "jpeg",
    quality: Optional[int] = None,
) -> None:
    """
    Converts an image to grayscale and saves the result.

    Args:
        image_path: The path to the input image file.
        output_path: The path to save the grayscale image.
        format (optional): Output format. Defaults to "jpeg".
        quality (optional): Compression quality 0-100. Uses format defaults if None.

    Returns:
        None
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("L")
            save_with_format(img, output_path, format, quality)
    except Exception as e:
        raise CorruptedFileError(f"Failed to process {image_path}: {e}")


def blur_image(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    format: str = "jpeg",
    quality: Optional[int] = None,
) -> None:
    """
    Apply a blur filter to an image and save the result.

    Args:
        image_path: The path to the input image file.
        output_path: The path to save the blurred image file.
        format (optional): Output format. Defaults to "jpeg".
        quality (optional): Compression quality 0-100. Uses format defaults if None.

    Returns:
        None
    """
    try:
        with Image.open(image_path) as img:
            img = img.filter(ImageFilter.BLUR)
            save_with_format(img, output_path, format, quality)
    except Exception as e:
        raise CorruptedFileError(f"Failed to process {image_path}: {e}")


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
    img: Image.Image, orientation: int
) -> tuple[Image.Image, bytes]:
    """
    Updates the orientation tag in the EXIF data dictionary to the specified value.

    Args:
        img: The image object to update.
        orientation: The orientation value to set (required).
    """
    exif_dict = piexif.load(img.info.get("exif", b""))
    exif_dict["0th"][piexif.ImageIFD.Orientation] = orientation
    exif_bytes = piexif.dump(exif_dict)
    img.info["exif"] = exif_bytes
    return img, exif_bytes


def rotate(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    format: str = "jpeg",
    quality: Optional[int] = None,
) -> None:
    """
    Rotates an image based on its EXIF orientation tag and preserves EXIF
    metadata.

    Args:
        image_path: Path to the input image.
        output_path: Path to save the output image.
        format (optional): Output format. Defaults to "jpeg".
        quality (optional): Compression quality 0-100. Uses format defaults if None.
    """
    try:
        rotated_img = None

        with Image.open(image_path) as img:
            # Extract EXIF data
            orientation = _extract_orientation(img)

            # Apply rotation based on EXIF orientation
            if orientation == 3:
                print(
                    f"{image_path}: Orientation is 3. Applying rotation of 180 degrees."
                )
                rotated_img = img.rotate(180)
            elif orientation == 6:
                print(
                    f"{image_path}: Orientation is 6. Applying rotation of 270 degrees."
                )
                rotated_img = img.rotate(270)
            elif orientation == 8:
                print(
                    f"{image_path}: Orientation is 8. Applying rotation of 90 degrees."
                )
                rotated_img = img.rotate(90)
            else:
                print(f"{image_path}: No rotation needed (orientation is 1).")

            final_img = rotated_img if rotated_img is not None else img

            # For JPEG with EXIF, preserve metadata
            if format.lower() in ["jpeg", "jpg"] and img.info.get("exif"):
                exif_updated_img, exif_bytes = _update_orientation(final_img, 1)
                exif_updated_img.save(
                    output_path, format="JPEG", exif=exif_bytes, quality=quality or 85
                )
            else:
                save_with_format(final_img, output_path, format, quality)
    except Exception as e:
        raise CorruptedFileError(f"Failed to process {image_path}: {e}")


def _print_processing_summary(
    successful: int,
    failed: int,
    errors: list,
    process_function: Callable,
    format: str,
    quality: Optional[int],
) -> None:
    """Print processing summary with Rich formatting."""
    console = Console()
    total = successful + failed
    task_name = process_function.__name__.replace("_", " ").title()

    console.print()  # Add spacing above summary

    if failed == 0:
        console.print("[green]✓ Processing complete![/green]")
        console.print(f"[green]  • Task: {task_name}[/green]")
        console.print(f"[green]  • Format: {format.upper()}[/green]")
        if quality:
            console.print(f"[green]  • Quality: {quality}%[/green]")
        console.print(f"[green]  • Images processed: {successful}/{total}[/green]")
    else:
        console.print("[green]✓ Processing complete with some errors[/green]")
        console.print(f"[green]  • Task: {task_name}[/green]")
        console.print(f"[green]  • Format: {format.upper()}[/green]")
        if quality:
            console.print(f"[green]  • Quality: {quality}%[/green]")
        console.print(
            f"[green]  • Successfully processed: {successful}/{total}[/green]"
        )
        console.print(f"[red]✗ Failed to process {failed} images:[/red]")
        for error in errors[:5]:  # Show first 5 errors
            console.print(f"[red]  • {error}[/red]")
        if len(errors) > 5:
            console.print(f"[red]  ... and {len(errors) - 5} more errors[/red]")


def process_images(
    image_folder: Union[str, Path],
    output_folder: Union[str, Path],
    process_function: Callable,
    format: str = "jpeg",
    quality: Optional[int] = None,
) -> None:
    """
    Processes images in a given folder using a specified processing function and
    saves the results to an output folder.

    Args:
        image_folder (str or Path): The path to the folder containing the input images.
        output_folder (str or Path): The path to the folder where the processed
            images will be saved.
        process_function (Callable): A function that processes the image.
        format (str): Output format for processed images.
        quality (int): Compression quality 0-100.

    Returns:
        None
    """
    output_path = Path(output_folder)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    image_files = [
        f.name
        for f in Path(image_folder).iterdir()
        if f.suffix.lower() in SUPPORTED_SUFFIXES
    ]

    if not image_files:
        print(f"No supported images found in {image_folder}")
        return

    successful = 0
    failed = 0
    errors = []

    with Progress() as progress:
        task = progress.add_task("[green]Processing Images...", total=len(image_files))

        with ThreadPoolExecutor() as executor:
            jobs = []
            for image_file in image_files:
                input_path = Path(image_folder) / image_file
                # Change extension based on output format
                output_name = Path(image_file).stem + f".{format}"
                output_file_path = Path(output_folder) / output_name

                job = executor.submit(
                    process_function, input_path, output_file_path, format, quality
                )
                jobs.append((job, input_path))

            for job in as_completed([j[0] for j in jobs]):
                try:
                    job.result()
                    successful += 1
                except Exception as e:
                    # Find the input_path for this job
                    input_path = next(path for j, path in jobs if j == job)
                    failed += 1
                    errors.append(f"{input_path}: {e}")

                progress.advance(task)

    _print_processing_summary(
        successful, failed, errors, process_function, format, quality
    )
