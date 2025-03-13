import argparse
from .main import (
    process_images, rotate, resize_image, grayscale_image, blur_image)


def main():
    parser = argparse.ArgumentParser(description="Process images.")
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

    # Map the task to the corresponding function
    task_function = {
        "rotate": rotate,
        "resize": resize_image,
        "grayscale": grayscale_image,
        "blur": blur_image,
    }[args.task]

    # Process the images
    process_images(args.input_folder, args.output_folder, task_function)


if __name__ == "__main__":
    main()
