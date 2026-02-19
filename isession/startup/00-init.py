# This file is executed when a new IPython session is started.
from os import environ
import tempfile
from pathlib import Path

import image_processor.main as ip


def list_image_dir(path=None):
    """List files in a directory. Defaults to IMAGE_PATH if no path provided."""
    target = Path(path) if path else Path(
        SAMPLE_IMAGE_DIR) if SAMPLE_IMAGE_DIR else Path('.')
    if target.is_dir():
        files = list(target.iterdir())
        for f in sorted(files):
            print(f"{'[D]' if f.is_dir() else '[F]'} {f.name}")
        print(f"\nTotal: {len(files)} items")
    else:
        print(f"Not a directory: {target}")


input_folder = environ.get("INPUT_FOLDER", None)
output_folder = environ.get("OUTPUT_FOLDER", None)

# Create useful constants
SAMPLE_IMAGE_DIR = input_folder
TEMP_OUTPUT_DIR = tempfile.mkdtemp()

print()

if input_folder is not None:
    print(f"Using input folder: {input_folder}")

if output_folder is not None:
    print(f"Using output folder: {output_folder}")

print(f"\nAvailable variables:")
print(f"  SAMPLE_IMAGE_PATH = {SAMPLE_IMAGE_DIR}")
print(f"  TEMP_OUTPUT_DIR = {TEMP_OUTPUT_DIR}")
print(f"  ip = image_processor.main module")
print(f"  Path = pathlib.Path")
print(f"  list_image_dir() = helper to list files (defaults to IMAGE_PATH)")
