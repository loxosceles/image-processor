from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageFilter
import argparse
from tqdm import tqdm
import piexif


def resize_image(image_path, output_path, size=(128, 128)):
    """
    Resize an image to the specified size and save it to the output path.

    Args:
        image_path (str): The path to the input image file.
        output_path (str): The path to save the resized image.
        size (tuple, optional): The desired size for the resized image. Defaults to (128, 128).

    Returns:
        None
    """
    with Image.open(image_path) as img:
        img = img.resize(size)
        img.save(output_path)


def grayscale_image(image_path, output_path):
    """
    Converts an image to grayscale and saves the result.

    Args:
        image_path (str): The path to the input image file.
        output_path (str): The path to save the grayscale image.

    Returns:
        None
    """
    with Image.open(image_path) as img:
        img = img.convert("L")
        img.save(output_path)


def blur_image(image_path, output_path):
    """
    Apply a blur filter to an image and save the result.

    Args:
        image_path (str): The path to the input image file.
        output_path (str): The path to save the blurred image file.

    Returns:
        None
    """
    with Image.open(image_path) as img:
        img = img.filter(ImageFilter.BLUR)
        img.save(output_path)

# Get the orientation tag


def _extract_orientation(img):
    """
    Extracts the orientation from the EXIF data dictionary.

    Args:
        exif_dict (dict): The EXIF data dictionary.

    Returns:
        int: The orientation value.
    """

    exif_dict = piexif.load(img.info.get("exif", b""))

    orientation = exif_dict.get("0th", {}).get(
        piexif.ImageIFD.Orientation, 1)
    return orientation


def _update_orientation(img, orientation=1):
    """
    Updates the orientation tag in the EXIF data dictionary to 1 (normal).

    Args:
        exif_dict (dict): The EXIF data dictionary.
    """
    exif_dict = piexif.load(img.info.get("exif", b""))
    exif_dict["0th"][piexif.ImageIFD.Orientation] = orientation
    exif_bytes = piexif.dump(exif_dict)
    img.info["exif"] = exif_bytes
    return img, exif_bytes


def rotate(image_path, output_path):
    """
    Rotates an image based on its EXIF orientation tag and preserves EXIF metadata.
    This version does not use a context manager.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
    """
    # Open the image with Pillow using a context manager
    print(f"Opening image {image_path}")
    rotated_img = None

    with Image.open(image_path) as img:
        # Extract EXIF data
        orientation = _extract_orientation(img)
        print(f"Orientation: {orientation}")

        # Apply rotation based on EXIF orientation
        if orientation == 3:
            print("Orientation is 3. Applying rotation of 180 degrees.")
            rotated_img = img.rotate(180)
        elif orientation == 6:
            print("Orientation is 6. Applying rotation of 270 degrees.")
            rotated_img = img.rotate(270)
        elif orientation == 8:
            print("Orientation is 8. Applying rotation of 90 degrees.")
            rotated_img = img.rotate(90)
        else:
            print("No rotation needed (orientation is 1).")

        exif_updated_img, exif_bytes = _update_orientation(rotated_img)

        # Save the rotated image with updated EXIF metadata
        exif_updated_img.save(output_path, exif=exif_bytes)


def process_images(image_folder, output_folder, process_function):
    """
    Processes images in a given folder using a specified processing function and
    saves the results to an output folder.

    Args:
        image_folder (str or Path): The path to the folder containing the input images.
        output_folder (str or Path): The path to the folder where the processed
            images will be saved.
        process_function (callable): A function that takes two arguments
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
        if f.suffix.lower() in {".jpg", ".png", ".jpeg"}
    ]

    with ThreadPoolExecutor() as executor:
        jobs = []
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

    process_images(args.input_folder, args.output_folder, task_function)
