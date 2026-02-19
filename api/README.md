# Image Processor API

FastAPI backend for the image processor web GUI.

## Quick Start

```bash
./dev-cli/manage.sh api
```

## Endpoints

### GET /health

Health check. Returns `{"status": "ok"}`

### POST /api/process

Process uploaded images.

**Parameters (multipart/form-data)**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| files | File[] | Yes | - | Image files (JPEG, PNG, WebP) |
| task | string | Yes | - | `resize`, `grayscale`, `blur`, `rotate` |
| format | string | No | `webp` | `jpeg`, `webp`, `png` |
| quality | int | No | format default | 0-100 compression quality |

**Response**: ZIP file containing processed images

**Response Headers**:
- `X-Processed-Count`: Successfully processed count
- `X-Error-Count`: Failed count

**Example**:

```bash
curl -X POST http://localhost:8000/api/process \
  -F "files=@image.jpg" \
  -F "task=grayscale" \
  -F "format=webp" \
  --output processed.zip
```

## Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
