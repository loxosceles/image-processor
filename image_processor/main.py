from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageFilter, ImageOps
import argparse
from exif import Image as ExifImage
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


def rotate_image_based_on_exif(image_path, output_path):
    """
    Rotates an image based on its EXIF orientation tag and preserves EXIF metadata.
    This version does not use a context manager.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
    """
    # Open the image with Pillow
    img = Image.open(image_path)
    print(f"Original image dimensions: {image_path}, {img.size}")

    # Extract EXIF data
    exif_dict = piexif.load(img.info.get("exif", b""))

    # Get the orientation tag
    orientation = exif_dict.get("0th", {}).get(piexif.ImageIFD.Orientation, 1)
    print(f"EXIF Orientation for {image_path}: {orientation}")

    # Apply rotation based on EXIF orientation
    if orientation == 2:
        print("Applying FLIP_LEFT_RIGHT")
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif orientation == 3:
        print("Applying 180° rotation")
        img = img.rotate(180)
    elif orientation == 4:
        print("Applying FLIP_TOP_BOTTOM")
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    elif orientation == 5:
        print("Applying FLIP_LEFT_RIGHT + 90° rotation")
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT).rotate(90, expand=True)
    elif orientation == 6:
        print("Applying 270° rotation (90° clockwise)")
        img = img.rotate(-90, expand=True)
    elif orientation == 7:
        print("Applying FLIP_LEFT_RIGHT + 270° rotation")
        img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT).rotate(-90, expand=True)
    elif orientation == 8:
        print("Applying 90° rotation (90° counterclockwise)")
        img = img.rotate(90, expand=True)
    else:
        print("No rotation needed (orientation is 1).")

    print(f"Image dimensions after rotation: {img.size}")

    # Update the orientation tag to 1 (normal) in the EXIF dictionary
    exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
    print(f"Updated EXIF Orientation: {exif_dict['0th'][piexif.ImageIFD.Orientation]}")

    # Convert the EXIF dictionary back to bytes
    exif_bytes = piexif.dump(exif_dict)

    # Save the rotated image with updated EXIF metadata
    img.save(output_path, exif=exif_bytes)
    print(f"Image saved to {output_path}")

    # Explicitly close the image
    img.close()


# def rotate_image_based_on_exif(image_path, output_path):
#     """
#     Rotates an image based on its EXIF orientation tag using `exiftool`.

#     Args:
#         image_path (str): Path to the input image.
#         output_path (str): Path to save the output image.
#     """
#     # Use exiftool to rotate the image and update the EXIF metadata
#     command = [
#         "exiftool",
#         "-Orientation=1",  # Set the orientation tag to 1 (normal)
#         "-n",  # Disable print conversion for numeric values
#         "-o",
#         output_path,  # Specify the output file
#         image_path,  # Specify the input file
#     ]

#     # Run the command
#     result = subprocess.run(command, capture_output=True, text=True)

#     # Check for errors
#     if result.returncode != 0:
#         print(f"Error rotating image: {result.stderr}")
#     else:
#         print(f"Image saved to {output_path}")

#     # Use exiftool to force rotation based on EXIF orientation
#     command_rotate = [
#         "exiftool",
#         "-Orientation=1",  # Set the orientation tag to 1 (normal)
#         "-n",  # Disable print conversion for numeric values
#         "-overwrite_original",  # Overwrite the output file
#         output_path,  # Specify the output file
#     ]

#     # Run the command
#     result_rotate = subprocess.run(command_rotate, capture_output=True, text=True)

#     # Check for errors
#     if result_rotate.returncode != 0:
#         print(f"Error forcing rotation: {result_rotate.stderr}")
#     else:
#         print(f"Rotation forced for {output_path}")


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
            jobs.append(executor.submit(process_function, input_path, output_path))

        # for job in tqdm(as_completed(jobs), total=len(jobs), desc="Processing Images"):
        #     try:
        #         job.result()
        #     except Exception as e:
        #         print(f"Error processing image: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Concurrent Image Processing")
    parser.add_argument("input_folder", help="Folder containing input images")
    parser.add_argument("output_folder", help="Folder to save processed images")
    parser.add_argument(
        "--task",
        choices=["rotate", "resize", "grayscale", "blur"],
        required=True,
        help="Image processing task",
    )

    args = parser.parse_args()

    task_function = {
        "rotate": rotate_image_based_on_exif,
        "resize": resize_image,
        "grayscale": grayscale_image,
        "blur": blur_image,
    }[args.task]

    process_images(args.input_folder, args.output_folder, task_function)
