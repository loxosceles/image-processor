# This file is executed when a new IPython session is started.
from os import environ

import image_processor.main as ip

input_folder = environ.get("INPUT_FOLDER", None)
output_folder = environ.get("OUTPUT_FOLDER", None)

print()

if input_folder is not None:
    print(f"Using input folder: {input_folder}")

if output_folder is not None:
    print(f"Using output folder: {output_folder}")
