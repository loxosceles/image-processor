FROM ghcr.io/astral-sh/uv:python3.11-alpine

# Set up directory structure to match expected paths
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy the image_processor dependency 
COPY image_processor ./image_processor

# Create API directory and copy files
RUN mkdir -p api
COPY api/uv.lock api/pyproject.toml ./api/

# Work from API directory so ../image_processor path works
WORKDIR /app/api

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the API code
COPY api/ .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH=".venv/bin:$PATH"

ARG API_PORT
ENV API_PORT=${API_PORT}

EXPOSE ${API_PORT}
CMD ["sh", "-c", "uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${API_PORT}"]