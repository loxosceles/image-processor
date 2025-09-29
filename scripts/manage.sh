#!/bin/bash
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

### Main functions
##
#
run() {
    local input_folder="$1"
    local output_folder="$2"
    local task="$3"
    local format="$4"
    local quality="$5"
    
    local cmd="docker compose run --rm image_processor uv run python -m image_processor.cli \"$input_folder\" \"$output_folder\" --task \"$task\""
    
    if [ -n "$format" ]; then
        cmd="$cmd --format \"$format\""
    fi
    
    if [ -n "$quality" ]; then
        cmd="$cmd --quality \"$quality\""
    fi
    
    eval "$cmd"
}

run_tests() {
    echo "Running pytests in ${ENVIRONMENT} environment"

    if [ "$ENVIRONMENT" = "dev" ]; then
        docker compose -f docker-compose.dev.yml run --rm image_processor uv run pytest -vvv
    else
        docker compose run --rm image_processor uv run pytest -vvv
    fi
}

build_and_push() {
    echo $GITHUB_PAT | docker login ghcr.io -u $GITHUB_USERNAME --password-stdin &&
        cd image_processor &&
        docker build -t image_processor . &&
        docker tag image_processor $DOCKER_REPOSITORY/image_processor:$TAG &&
        docker push $DOCKER_REPOSITORY/image_processor:$TAG
}

isession() {
    docker compose run --rm -it isession
}

# Quick dev execution
run_image_processor() {
    cd image_processor
    uv run python -m image_processor.cli "$@"
}

# Complete package build flow
build_package() {
    echo "Building package..."
    cd image_processor
    uv build
    echo "Installing package..."
    uv tool install dist/*.whl --force
    echo "Package built and installed successfully!"
    echo "You can now use: image-processor"
}

### Helper functions
##
#
_check_mutually_exclusive_args() {
    local run_count=0
    local build_count=0

    for arg in "$@"; do
        case "$arg" in
        run)
            run_count=$((run_count + 1))
            ;;
        build)
            build_count=$((build_count + 1))
            ;;
        esac
    done

    if [ "$run_count" -gt 0 ] && [ "$build_count" -gt 0 ]; then
        echo "Error: 'run' and 'build' cannot be used together."
        exit 1
    fi
}

_check_run_args() {
    local allowed_args=("$@")
    local missing_args=()
    for arg in "${allowed_args[@]}"; do
        if [ -z "${!arg}" ]; then
            missing_args+=("$arg")
        fi
    done

    if [ ${#missing_args[@]} -ne 0 ]; then
        echo "Error: Missing required arguments: ${missing_args[*]}"
        exit 1
    fi
}

die() {
    local _ret="${2:-1}"
    test "${_PRINT_HELP:-no}" = yes && print_help >&2
    echo "$1" >&2
    exit "${_ret}"
}

begins_with_short_option() {
    local first_option all_short_options='iotfqh'
    first_option="${1:0:1}"
    test "$all_short_options" = "${all_short_options/$first_option/}" && return 1 || return 0
}

print_help_run() {
    printf '%s\n' "  run:"
    printf '\t%s\n' "-i, --input <arg>   Input folder (required)"
    printf '\t%s\n' "-o, --output <arg>  Output folder (required)"
    printf '\t%s\n' "-t, --task <arg>    Task to perform (required)"
    printf '\t%s\n' "-f, --format <arg>  Output format: jpeg, webp, png (default: jpeg)"
    printf '\t%s\n' "-q, --quality <arg> Compression quality 0-100 (default: 85 for JPEG, 80 for WebP)"
    printf '\t%s\n' "-h, --help          Prints help for the 'run' scope"
}

print_help_dev() {
    printf '%s\n' "  dev:"
    printf '\t%s\n' "--isession          Start an interactive session (required)"
    printf '\t%s\n' "-h, --help          Prints help for the 'dev' scope"
}

print_help_build() {
    printf '%s\n' "  build:"
    printf '\t%s\n' "-h, --help          Prints help for the 'build' scope"
}

print_help_image_processor() {
    printf '%s\n' "  image_processor:"
    printf '\t%s\n' "Direct arguments passed to CLI (no flags needed)"
    printf '\t%s\n' "Example: manage.sh image_processor input output --task resize --format webp"
    printf '\t%s\n' "-h, --help          Prints help for the 'image_processor' scope"
}

print_help_package() {
    printf '%s\n' "  package:"
    printf '\t%s\n' "Build and install the package (no additional arguments)"
    printf '\t%s\n' "-h, --help          Prints help for the 'package' scope"
}

print_help() {
    printf '%s\n' "Usage: $0 <scope> [options]"
    printf '\n%s\n' "Scopes:"
    printf '\t%s\n' "run             - Process images with input, output, and task arguments"
    printf '\t%s\n' "build           - Build and push the Docker image (no additional arguments)"
    printf '\t%s\n' "dev             - Start an interactive development session"
    printf '\t%s\n' "image_processor - Quick dev execution (pass CLI args directly)"
    printf '\t%s\n' "package         - Build and install the complete package"
    printf '\n%s\n' "Scope-specific options:"

    # Interpolate scope-specific help texts
    print_help_run
    print_help_build
    print_help_dev
    print_help_image_processor
    print_help_package

    printf '\n%s\n' "Global options:"
    printf '\t%s\n' "-h, --help          Prints this help message"
}

parse_commandline_run() {
    while test $# -gt 0; do
        _key="$1"
        case "$_key" in
        -i | --input)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_input="$2"
            shift
            ;;
        --input=*)
            _arg_input="${_key##--input=}"
            ;;
        -i*)
            _arg_input="${_key##-i}"
            ;;
        -o | --output)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_output="$2"
            shift
            ;;
        --output=*)
            _arg_output="${_key##--output=}"
            ;;
        -o*)
            _arg_output="${_key##-o}"
            ;;
        -t | --task)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_task="$2"
            shift
            ;;
        --task=*)
            _arg_task="${_key##--task=}"
            ;;
        -t*)
            _arg_task="${_key##-t}"
            ;;
        -f | --format)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_format="$2"
            shift
            ;;
        --format=*)
            _arg_format="${_key##--format=}"
            ;;
        -f*)
            _arg_format="${_key##-f}"
            ;;
        -q | --quality)
            test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
            _arg_quality="$2"
            shift
            ;;
        --quality=*)
            _arg_quality="${_key##--quality=}"
            ;;
        -q*)
            _arg_quality="${_key##-q}"
            ;;
        -h | --help)
            print_help_run
            exit 0
            ;;
        -h*)
            print_help_run
            exit 0
            ;;
        *)
            _PRINT_HELP=yes die "FATAL ERROR: Got an unexpected argument '$1'" 1
            ;;
        esac
        shift
    done
}

parse_commandline_build() {
    while test $# -gt 0; do
        _key="$1"
        case "$_key" in
        -h | --help)
            print_help_build
            exit 0
            ;;
        -h*)
            print_help_build
            exit 0
            ;;
        *)
            exit 0
            ;;
        esac
        shift
    done
}

parse_commandline_test() {
    while test $# -gt 0; do
        _key="$1"
        case "$_key" in
        -h | --help)
            print_help_build
            exit 0
            ;;
        -h*)
            print_help_build
            exit 0
            ;;
        *)
            exit 0
            ;;
        esac
        shift
    done
}

parse_commandline_dev() {
    while test $# -gt 0; do
        _key="$1"
        case "$_key" in
        --isession)
            _arg_isession=1 # Set _arg_isession to 1 (true) when --isession is provided
            ;;
        -h | --help)
            print_help_dev
            exit 0
            ;;
        -h*)
            print_help_dev
            exit 0
            ;;
        *)
            _PRINT_HELP=yes die "FATAL ERROR: Got an unexpected argument '$1'" 1
            ;;
        esac
        shift
    done
}

# _check_mutually_exclusive_args "$@"

if [ "$1" = "run" ]; then
    shift
    parse_commandline_run "$@"
    scope_args=("_arg_input" "_arg_output" "_arg_task")
    _check_run_args "${scope_args[@]}"
    run "$_arg_input" "$_arg_output" "$_arg_task" "$_arg_format" "$_arg_quality"
    exit 0

elif [ "$1" = "build" ]; then
    shift
    parse_commandline_build "$@"
    if [ "$#" -ne 0 ]; then
        echo "Error: 'build' does not take any additional arguments."
        exit 1
    fi
    build_and_push
    exit 0

elif [ "$1" = "dev" ]; then
    shift
    parse_commandline_dev "$@"
    scope_args=("_arg_isession")
    _check_run_args "${scope_args[@]}"
    isession
    exit 0

elif [ "$1" = "test" ]; then
    shift
    parse_commandline_test "$@"
    if [ "$#" -ne 0 ]; then
        echo "Error: 'test' does not take any additional arguments."
        exit 1
    fi
    run_tests
    exit 0

elif [ "$1" = "image_processor" ]; then
    shift
    run_image_processor "$@"
    exit 0

elif [ "$1" = "package" ]; then
    shift
    if [ "$#" -ne 0 ]; then
        echo "Error: 'package' does not take any additional arguments."
        exit 1
    fi
    build_package
    exit 0

else
    print_help
    exit 1
fi
