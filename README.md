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

The image processor features a [Click-based CLI](https://click.palletsprojects.com/) for easy command-line usage.

### Get Help

```bash
# Beautiful help output
image-processor --help

# Or during development
uv run python -m image_processor.cli --help
```

### Basic Usage

```bash
# Basic image processing
image-processor <input-dir> --output <output-dir> --task resize

# Web optimization: Convert to WebP with quality control
image-processor <input-dir> --output <output-dir> --task resize --format webp --quality 80

# High quality JPEG for print
image-processor <input-dir> --output <output-dir> --task resize --format jpeg --quality 95

# Create grayscale thumbnails in WebP format
image-processor <input-dir> --output <output-dir> --task grayscale --format webp --quality 75
```

### Web Developer Examples

```bash
# Convert images to WebP for faster loading
image-processor <input-dir> --output <output-dir> --task resize --format webp --quality 80

# Create JPEG fallbacks for older browsers
image-processor <input-dir> --output <output-dir> --task resize --format jpeg --quality 85

# Optimize images with progressive JPEG
image-processor <input-dir> --output <output-dir> --task resize --format jpeg --quality 85

# Batch convert to compressed WebP
image-processor <input-dir> --output <output-dir> --task resize --format webp --quality 70
```

## Available Options

- `--output`: Output directory (required, must exist and be empty)
- `--task`: `resize`, `grayscale`, `blur`, `rotate` (required)
- `--format`: `jpeg`, `webp`, `png` (default: jpeg)
- `--quality`: 0-100 compression quality (default: 85 for JPEG, 80 for WebP)

## Important Requirements

- **Output directory must exist and be empty**: Prevents accidental file overwrites
- **No automatic directory creation**: Ensures intentional output placement

## Development

This project uses a devcontainer configuration for VSCode with `chezmoi` for dotfile management. See [devcontainer_template](https://github.com/loxosceles/devcontainer_config_template) for details.

### Development Commands (manage.sh)

The `manage.sh` script is for **development only** and handles development workflows:

```bash
# Quick development (uses new --output interface)
manage.sh image_processor <input-dir> --output <output-dir> --task resize --format webp

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
manage.sh image_processor <input-dir> --output <output-dir> --task resize --format webp

# Run tests (uses volume mounting for instant feedback)
manage.sh test

# Test final package
manage.sh package
image-processor <input-dir> --output <output-dir> --task resize --format webp

# Run tests locally without Docker
uv run pytest
```

## CI/CD

The project includes GitHub Actions for continuous integration:

- **Automated Testing**: Tests run automatically on push/PR to `main` and `dev` branches
- **Docker-based CI**: Uses the same Docker environment as local development
- **Volume Mounting**: Fast test execution without rebuilding containers
