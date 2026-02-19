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
    # Validate required environment variables
    if [ -z "$DOCKER_REPOSITORY" ] || [ -z "$TAG" ] || [ -z "$API_PORT" ] || [ -z "$FRONTEND_PORT" ] || [ -z "$API_URL" ]; then
        echo "Error: Missing required environment variables. Make sure .env is properly configured."
        echo "Required: DOCKER_REPOSITORY, TAG, API_PORT, FRONTEND_PORT, API_URL"
        exit 1
    fi
    
    local no_cache="$1"
    local cache_flag=""
    
    if [[ "$no_cache" == "--no-cache" ]]; then
        echo "Building with no cache"
        cache_flag="--no-cache"
    else
        echo "Building with cache (default)"
    fi
    
    # Build all images first (without login)
    docker build $cache_flag -t image_processor ./image_processor &&
        docker tag image_processor $DOCKER_REPOSITORY/image_processor:$TAG

    docker build $cache_flag --build-arg API_PORT=$API_PORT -f api/Dockerfile -t image_processor_api . &&
        docker tag image_processor_api $DOCKER_REPOSITORY/image_processor_api:$TAG

    docker build $cache_flag --build-arg FRONTEND_PORT=$FRONTEND_PORT --build-arg API_URL=$API_URL -f frontend/Dockerfile -t image_processor_frontend . &&
        docker tag image_processor_frontend $DOCKER_REPOSITORY/image_processor_frontend:$TAG

    # Login and push after building
    docker login ghcr.io -u $GITHUB_USERNAME --password-stdin <<EOF
$GITHUB_PAT
EOF
    
    docker push $DOCKER_REPOSITORY/image_processor:$TAG
    docker push $DOCKER_REPOSITORY/image_processor_api:$TAG
    docker push $DOCKER_REPOSITORY/image_processor_frontend:$TAG
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
    uv pip install dist/*.whl --force-reinstall
    echo "Package built and installed successfully!"
    echo "You can now use: image-processor"
}

cmd_dev() {
    echo "Starting DEVELOPMENT servers..."
    docker compose -f docker-compose.dev.yml up --build
}

cmd_start() {
    echo "Starting PRODUCTION servers..."
    docker compose up
}

cmd_stop() {
    echo "Stopping all image processor servers..."
    docker compose -f docker-compose.dev.yml down 2>/dev/null || true
    docker compose down 2>/dev/null || true
    echo "All servers stopped"
}

cmd_api() {
    echo "Starting API server only..."
    docker compose -f docker-compose.dev.yml up --build api
}

cmd_frontend() {
    echo "Starting frontend server only..."
    docker compose -f docker-compose.dev.yml up --build frontend
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
cmd_build_local() {
    # Validate required environment variables
    if [ -z "$DOCKER_REPOSITORY" ] || [ -z "$TAG" ] || [ -z "$API_PORT" ] || [ -z "$FRONTEND_PORT" ] || [ -z "$API_URL" ]; then
        echo "Error: Missing required environment variables. Make sure .env is properly configured."
        echo "Required: DOCKER_REPOSITORY, TAG, API_PORT, FRONTEND_PORT, API_URL"
        exit 1
    fi
    
    echo "Building all images locally..."
    
    # Build image_processor
    docker build -t $DOCKER_REPOSITORY/image_processor:$TAG ./image_processor
    
    # Build API
    docker build --build-arg API_PORT=$API_PORT -f api/Dockerfile -t $DOCKER_REPOSITORY/image_processor_api:$TAG .
    
    # Build frontend  
    docker build --build-arg FRONTEND_PORT=$FRONTEND_PORT --build-arg API_URL=$API_URL -f frontend/Dockerfile -t $DOCKER_REPOSITORY/image_processor_frontend:$TAG .
    
    echo "All images built locally"
}