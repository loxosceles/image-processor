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
    docker login ghcr.io -u $GITHUB_USERNAME --password-stdin <<EOF
$GITHUB_PAT
EOF
    cd image_processor &&
        docker build -t image_processor . &&
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
