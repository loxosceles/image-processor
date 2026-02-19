#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Core command implementations - pure business logic, no CLI dependencies

cmd_run_tests() {
    echo "Running pytests in ${ENVIRONMENT} environment"
    if [ "$ENVIRONMENT" = "dev" ]; then
        docker compose -f docker-compose.dev.yml run --rm \
            -v "$(pwd)/image_processor/tests:/app/tests:ro" \
            -v "$(pwd)/image_processor/image_processor:/app/image_processor:ro" \
            image_processor uv run pytest -vvv
    else
        docker compose run --rm \
            -v "$(pwd)/image_processor/tests:/app/tests:ro" \
            -v "$(pwd)/image_processor/image_processor:/app/image_processor:ro" \
            image_processor uv run pytest -vvv
    fi
}

cmd_build_and_push() {
    local no_cache="$1"
    local cache_flag=""
    
    if [[ "$no_cache" == "--no-cache" ]]; then
        echo "Building with no cache"
        cache_flag="--no-cache"
    else
        echo "Building with cache (default)"
    fi
    
    docker login ghcr.io -u $GITHUB_USERNAME --password-stdin <<EOF
$GITHUB_PAT
EOF
    cd image_processor &&
        docker build $cache_flag -t image_processor . &&
        docker tag image_processor $DOCKER_REPOSITORY/image_processor:$TAG &&
        docker push $DOCKER_REPOSITORY/image_processor:$TAG
}

cmd_isession() {
    docker compose run --rm -it isession
}

cmd_run_image_processor() {
    local input_path="$1"
    local args=("${@:2}")
    
    # Convert relative input path to absolute path
    [[ "$input_path" != /* ]] && input_path="$(pwd)/$input_path"
    
    # Find and convert --output path to absolute if relative
    for ((i=0; i<${#args[@]}; i++)); do
        if [[ "${args[i]}" == "--output" && $((i+1)) -lt ${#args[@]} ]]; then
            local output_path="${args[i+1]}"
            [[ "$output_path" != /* ]] && args[i+1]="$(pwd)/$output_path"
            break
        fi
    done
    
    (cd image_processor && uv run python -m image_processor.cli "$input_path" "${args[@]}")
}

cmd_build_package() {
    echo "Building package..."
    cd image_processor
    uv build
    echo "Installing package..."
    uv tool install dist/*.whl --force
    echo "Package built and installed successfully!"
    echo "You can now use: image-processor"
}

cmd_api() {
    local api_port="${API_PORT:-7432}"
    echo "Starting API server on port $api_port..."
    cd api && uv sync && uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:$api_port"
}

cmd_frontend() {
    local api_port="${API_PORT:-7432}"
    local frontend_port="${FRONTEND_PORT:-7433}"
    echo "Starting frontend dev server on port $frontend_port..."
    cd frontend && export NEXT_PUBLIC_API_URL="http://localhost:$api_port" && pnpm install && pnpm dev --port "$frontend_port"
}

cmd_dev() {
    # Load ports from .env
    local api_port="${API_PORT:-7432}"
    local frontend_port="${FRONTEND_PORT:-7433}"
    
    # Check if ports are in use
    if lsof -i ":$api_port" >/dev/null 2>&1; then
        echo "Error: Port $api_port is already in use. Stop the existing process or change API_PORT in .env"
        exit 1
    fi
    
    if lsof -i ":$frontend_port" >/dev/null 2>&1; then
        echo "Error: Port $frontend_port is already in use. Stop the existing process or change FRONTEND_PORT in .env"
        exit 1
    fi
    
    echo "Starting DEVELOPMENT servers..."
    echo "API:      http://localhost:$api_port (uvicorn with hot reload)"
    echo "Frontend: http://localhost:$frontend_port (Next.js dev server)"
    echo ""
    echo "Press Ctrl+C to stop both servers"
    
    # Proper cleanup with flag to prevent multiple executions
    cleanup_done=false
    cleanup() {
        if [ "$cleanup_done" = true ]; then
            return
        fi
        cleanup_done=true
        echo ""
        echo "Shutting down..."
        kill 0 2>/dev/null
        exit 0
    }
    trap cleanup EXIT INT TERM
    
    # Start DEVELOPMENT servers
    (cd api && uv sync && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port "$api_port") &
    (cd frontend && export NEXT_PUBLIC_API_URL="http://localhost:$api_port" && export NODE_ENV=development && pnpm install && pnpm dev --port "$frontend_port") &
    
    wait
}

cmd_lint() {
    echo "Running linters..."
    (cd image_processor && uv run ruff check image_processor/)
    (cd api && uv run ruff check app/)
}

cmd_test_api() {
    echo "Running API tests..."
    cd api && uv sync --all-extras && uv run pytest -v
}

cmd_start() {
    # Load ports from .env
    local api_port="${API_PORT:-7432}"
    local frontend_port="${FRONTEND_PORT:-7433}"
    
    # Check if ports are in use
    if lsof -i ":$api_port" >/dev/null 2>&1; then
        echo "Error: Port $api_port is already in use. Stop the existing process or change API_PORT in .env"
        exit 1
    fi
    
    if lsof -i ":$frontend_port" >/dev/null 2>&1; then
        echo "Error: Port $frontend_port is already in use. Stop the existing process or change FRONTEND_PORT in .env"
        exit 1
    fi
    
    echo "Building frontend for production..."
    (cd frontend && export NEXT_PUBLIC_API_URL="http://localhost:$api_port" && export NODE_ENV=production && pnpm install && pnpm build)
    
    if [ $? -ne 0 ]; then
        echo "Frontend build failed"
        exit 1
    fi
    
    echo "Starting PRODUCTION servers..."
    echo "API:      http://localhost:$api_port (gunicorn with 4 workers)"
    echo "Frontend: http://localhost:$frontend_port (Next.js production server)"
    echo ""
    echo "Press Ctrl+C to stop both servers"
    
    # Proper cleanup with flag to prevent multiple executions
    cleanup_done=false
    cleanup() {
        if [ "$cleanup_done" = true ]; then
            return
        fi
        cleanup_done=true
        echo ""
        echo "Shutting down..."
        kill 0 2>/dev/null
        exit 0
    }
    trap cleanup EXIT INT TERM
    
    # Start PRODUCTION servers
    (cd api && uv sync && uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind "0.0.0.0:$api_port") &
    (cd frontend && export NEXT_PUBLIC_API_URL="http://localhost:$api_port" && export NODE_ENV=production && pnpm start -p "$frontend_port") &
    
    wait
}
