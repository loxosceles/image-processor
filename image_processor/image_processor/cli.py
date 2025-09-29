import argparse
from .main import (
    process_images, rotate, resize_image, grayscale_image, blur_image)


def main():
    parser = argparse.ArgumentParser(description="Process images with web optimization.")
    parser.add_argument("input_folder", help="Folder containing input images")
    parser.add_argument("output_folder", help="Folder to save processed images")
    parser.add_argument(
        "--task",
        choices=["rotate", "resize", "grayscale", "blur"],
        required=True,
        help="Image processing task",
    )
    parser.add_argument(
        "--format",
        choices=["jpeg", "webp", "png"],
        default="jpeg",
        help="Output format (default: jpeg)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        help="Compression quality 0-100 (default: 85 for JPEG, 80 for WebP)",
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
    try:
        process_images(
            args.input_folder, 
            args.output_folder, 
            task_function,
            args.format,
            args.quality
        )
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
    except Exception as e:
        print(f"\nFatal error: {e}")


if __name__ == "__main__":
    main()
