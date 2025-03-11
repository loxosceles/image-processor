# Image Processor

## Description

This is a simple image processor that can be used to apply filters to images. It operates on batches of images by applying the same filter to all images in the input folder. The filters that can be applied are:

- Grayscale
- Rotate
- Resize
- Blur

## Setup

You can run the application without any setup by using the Docker image that is
available on the Github Container Registry. However, if you want to build the
image yourself, you can do so by configuring your own docker repository and
running the `manage.sh build` command. See the `.env.template`file for the
environment variables that need to be set.

## Usage

The processor can be run from the command line and the user can specify the input folder, output folder, filter to apply and the filter parameters.
The processor runs inside a Docker container, so the user needs to have Docker
installed on their machine. For convenience, there is a `manage.sh` script that
can be used to run the processor.

Example:

```bash
# For these examples, I assume that you have added the scripts folder to the PATH, e.g., by running: `export PATH=${PWD}/scripts:$PATH` from the root of the project.

# First, run the help command to see the available options:
manage.sh --help

# To run the processor with the blur filter on the images in the `images` folder and save the processed images in the `processed` folder:
manage.sh run -i images -o processed -t blur

# Or, using the long options:
manage.sh run --input images --output processed --filter blur

# Drop into an interactive iPython session inside the container:
manage.sh dev --isession

# Build a new image from the Dockerfile and push it to the Github Container Registry:
manage.sh build
```

## Further Development

This is WIP. While the current implementation is only meant as a demo project, I
might add more features in the future for it to become a more useful tool.
