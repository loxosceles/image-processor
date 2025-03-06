from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageFilter
import argparse
from tqdm import tqdm


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
        if f.suffix in {".jpg", ".png", ".jpeg"}
    ]

    with ThreadPoolExecutor() as executor:
        futures = []
        for image_file in image_files:
            input_path = Path(image_folder) / image_file
            output_path = Path(output_folder) / image_file
            futures.append(executor.submit(process_function, input_path, output_path))

        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing Images"
        ):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing image: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concurrent Image Processing")
    parser.add_argument("input_folder", help="Folder containing input images")
    parser.add_argument("output_folder", help="Folder to save processed images")
    parser.add_argument(
        "--task",
        choices=["resize", "grayscale", "blur"],
        required=True,
        help="Image processing task",
    )

    args = parser.parse_args()

    task_function = {
        "resize": resize_image,
        "grayscale": grayscale_image,
        "blur": blur_image,
    }[args.task]

    process_images(args.input_folder, args.output_folder, task_function)
