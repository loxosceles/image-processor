import click
from .main import (
    process_images, rotate, resize_image, grayscale_image, blur_image)


@click.command()
@click.argument('input_folder')
@click.argument('output_folder')
@click.option('--task', 
              type=click.Choice(['rotate', 'resize', 'grayscale', 'blur']), 
              required=True,
              help='Image processing task')
@click.option('--format', 'output_format',
              type=click.Choice(['jpeg', 'webp', 'png']), 
              default='jpeg',
              help='Output format (default: jpeg)')
@click.option('--quality', 
              type=int,
              help='Compression quality 0-100 (default: 85 for JPEG, 80 for WebP)')
def main(input_folder, output_folder, task, output_format, quality):
    """Process images with web optimization.
    
    INPUT_FOLDER   Folder containing input images
    OUTPUT_FOLDER  Folder to save processed images
    """
    task_function = {
        "rotate": rotate,
        "resize": resize_image,
        "grayscale": grayscale_image,
        "blur": blur_image,
    }[task]

    try:
        process_images(
            input_folder, 
            output_folder, 
            task_function,
            output_format,
            quality
        )
    except KeyboardInterrupt:
        click.echo("\nProcessing interrupted by user", err=True)
    except Exception as e:
        click.echo(f"\nFatal error: {e}", err=True)


if __name__ == "__main__":
    main()
