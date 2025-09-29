# Image Processor

## Description

A web developer-focused image processor for batch optimization and format conversion. Designed to streamline common web development workflows like creating WebP images, responsive thumbnails, and optimized assets.

Supported operations:
- **Resize** - Create thumbnails and responsive images
- **Format conversion** - JPEG, WebP, PNG with quality control
- **Grayscale** - Convert to monochrome
- **Rotate** - Auto-correct orientation from EXIF data
- **Blur** - Apply blur effects
- **Web optimization** - Progressive JPEG, WebP compression

## Setup

You can run the application without any setup by using the Docker image that is
available on the Github Container Registry. However, if you want to build the
image yourself, you can do so by configuring your own docker repository and
running the `manage.sh build` command. See the `.env.template` file for the
environment variables that need to be set. As for all `.template` files in this
repository, just copy that file, remove the `.template` extension, and fill in
the values.

```bash

## Usage

The processor can be run from the command line and the user can specify the input folder, output folder, filter to apply and the filter parameters.
The processor runs inside a Docker container, so the user needs to have Docker
installed on their machine. For convenience, there is a `manage.sh` script that
can be used to run the processor.

## Basic Usage

```bash
# Add scripts to PATH for convenience
export PATH=${PWD}/scripts:$PATH

# Basic image processing (defaults to JPEG output)
manage.sh run -i images -o processed --task resize

# Web optimization: Convert to WebP with quality control
manage.sh run -i images -o web-ready --task resize --format webp --quality 80

# High quality JPEG for print
manage.sh run -i photos -o print --task resize --format jpeg --quality 95

# Create grayscale thumbnails in WebP format
manage.sh run -i gallery -o thumbnails --task grayscale --format webp --quality 75
```

## Web Developer Examples

```bash
# Convert product images to WebP for faster loading
manage.sh run -i product-photos -o webp-catalog --task resize --format webp --quality 80

# Create JPEG fallbacks for older browsers
manage.sh run -i product-photos -o jpeg-fallback --task resize --format jpeg --quality 85

# Optimize blog images with progressive JPEG
manage.sh run -i blog-images -o optimized --task resize --format jpeg --quality 85

# Batch convert PNG screenshots to compressed WebP
manage.sh run -i screenshots -o compressed --task resize --format webp --quality 70
```

## Available Options

- `--task`: `resize`, `grayscale`, `blur`, `rotate`
- `--format`: `jpeg`, `webp`, `png` (default: jpeg)
- `--quality`: 0-100 compression quality (default: 85 for JPEG, 80 for WebP)

## Development Commands

```bash
# Get help
manage.sh --help

# Interactive development session
manage.sh dev --isession

# Run tests
manage.sh test

# Build and push Docker image
manage.sh build
```

## Features

### ✅ Phase 1 (Current)
- **WebP Support** - Modern format for 25-35% smaller file sizes
- **Quality Control** - Fine-tune compression (0-100 scale)
- **Progressive JPEG** - Better loading experience for web
- **Robust Error Handling** - Continues processing on failures, detailed reporting
- **Format Conversion** - JPEG ↔ WebP ↔ PNG with quality preservation

### 🚧 Coming Soon (Phase 2)
- **Responsive Image Sets** - Generate multiple sizes at once
- **Web Presets** - One-command optimization for common scenarios
- **Batch Operations** - Chain multiple filters in single command

## Web Optimization Benefits

- **Faster Loading**: WebP images are 25-35% smaller than JPEG
- **Progressive Enhancement**: JPEG fallbacks for older browsers
- **Batch Processing**: Process hundreds of images in seconds
- **Quality Control**: Perfect balance between file size and visual quality
- **Modern Formats**: Ready for responsive images and `<picture>` elements

## Development

This project uses a devcontainer configuration for VSCode with `chezmoi` for dotfile management. See [devcontainer_template](https://github.com/loxosceles/devcontainer_config_template) for details.

Use `docker-compose.dev.yml` for local development.
