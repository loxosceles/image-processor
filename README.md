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

## Installation

### For Users
```bash
# Install with uv (recommended)
cd image_processor
uv sync

# Or install with pip
pip install -e .
```

### For Developers
Use the Docker setup with `manage.sh` for development, building, and testing.

## Usage

The image processor features a beautiful Click-based CLI for easy command-line usage.

### Get Help
```bash
# Beautiful help output
image-processor --help

# Or during development
uv run python -m image_processor.cli --help
```

### Basic Usage

```bash
# Basic image processing (defaults to JPEG output)
image-processor images processed --task resize

# Web optimization: Convert to WebP with quality control
image-processor images web-ready --task resize --format webp --quality 80

# High quality JPEG for print
image-processor photos print --task resize --format jpeg --quality 95

# Create grayscale thumbnails in WebP format
image-processor gallery thumbnails --task grayscale --format webp --quality 75
```

### Web Developer Examples

```bash
# Convert product images to WebP for faster loading
image-processor product-photos webp-catalog --task resize --format webp --quality 80

# Create JPEG fallbacks for older browsers
image-processor product-photos jpeg-fallback --task resize --format jpeg --quality 85

# Optimize blog images with progressive JPEG
image-processor blog-images optimized --task resize --format jpeg --quality 85

# Batch convert PNG screenshots to compressed WebP
image-processor screenshots compressed --task resize --format webp --quality 70
```

## Available Options

- `--task`: `resize`, `grayscale`, `blur`, `rotate`
- `--format`: `jpeg`, `webp`, `png` (default: jpeg)
- `--quality`: 0-100 compression quality (default: 85 for JPEG, 80 for WebP)

## Development

This project uses a devcontainer configuration for VSCode with `chezmoi` for dotfile management. See [devcontainer_template](https://github.com/loxosceles/devcontainer_config_template) for details.

### Development Commands (manage.sh)

The `manage.sh` script is for **developers only** and handles development workflows:

```bash
# Quick development (replaces long uv commands)
manage.sh image_processor input_folder output_folder --task resize --format webp

# Build and install complete package
manage.sh package

# Interactive development session
manage.sh dev --isession

# Run tests
manage.sh test

# Build and push Docker image
manage.sh build

# Get help
manage.sh --help
```

### Development Workflow
```bash
# Quick development (instant changes)
manage.sh image_processor input_folder output_folder --task resize --format webp

# Test final package
manage.sh package
image-processor input_folder output_folder --task resize --format webp

# Run tests
uv run pytest
```

## Features

### ✅ Phase 1 (Current)
- **Beautiful CLI** - Modern Click-based interface with helpful output
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


