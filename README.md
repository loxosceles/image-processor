# Image Processor

## Description

This is a simple image processor that can be used to apply filters to images. It operates on batches of images by applying the same filter to all images in the input folder. The filters that can be applied are:

- Grayscale
- Rotate
- Resize
- Blur

The processor can be run from the command line and the user can specify the input folder, output folder, filter to apply and the filter parameters.
The processor can be run as a Docker container.

Example usage:

```bash
docker compose run --rm image_processor <INPUT_FOLDER> <OUTPUT_FOLDER> --task grayscale
```

## Development

This is WIP. While the current implementation is only meant as a demo project, I might add more features in the future for it to become a more useful tool.
