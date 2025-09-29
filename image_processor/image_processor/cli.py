import click
from pathlib import Path
from .main import (
    process_images, rotate, resize_image, grayscale_image, blur_image)


@click.command()
@click.argument('input_folder')
@click.option('--output', 'output_folder',
              required=True,
              help='Output folder to save processed images (must exist and be empty)')
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
    """
    # Validate output directory exists
    if not Path(output_folder).exists():
        click.echo(f"Error: Output directory '{output_folder}' does not exist.", err=True)
        raise click.Abort()
    
    # Validate output directory is empty
    if any(Path(output_folder).iterdir()):
        click.echo(f"Error: Output directory '{output_folder}' is not empty.", err=True)
        click.echo("Please use an empty directory to avoid overwriting files.", err=True)
        raise click.Abort()

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
