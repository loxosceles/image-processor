#!/usr/bin/env bash

# Handle help before sourcing to avoid errors
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        echo "Development management script"
        echo ""
        echo "USAGE: manage.sh <command> [options]"
        echo ""
        echo "COMMANDS:"
        echo "  build [--no-cache] Build and push Docker image to registry"
        echo "  help           Show this help message"
        echo "  isession       Start interactive development session"
        echo "  test           Run pytest suite with volume mounting"
        echo "  image_processor Run image processor with arguments"
        echo "  package        Build and install package locally"
        echo ""
        echo "EXAMPLES:"
        echo "  manage.sh help"
        echo "  manage.sh isession"
        echo "  manage.sh test"
        echo "  manage.sh image_processor images/ --output processed/ --task resize"
        echo "  manage.sh image_processor images/ --output processed/ --task resize --format webp --quality 80"
        exit 0
fi


# Global variables
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/commands.sh"

# Created by argbash-init v2.11.0
# ARG_POSITIONAL_SINGLE([command])
# ARG_LEFTOVERS([args])
# ARG_DEFAULTS_POS()
# ARG_HELP([Development management script for image processor])
# ARGBASH_GO()

# Command routing
case "$_arg_command" in
    "build") 
        if [[ "${_arg_leftovers[0]}" == "--no-cache" ]]; then
            cmd_build_and_push "--no-cache"
        else
            cmd_build_and_push
        fi
        ;;
    "help") 
        echo "Development management script"
        echo ""
        echo "USAGE: manage.sh <command> [options]"
        echo ""
        echo "COMMANDS:"
        echo "  build [--no-cache] Build and push Docker image to registry"
        echo "  help           Show this help message"
        echo "  isession       Start interactive development session"
        echo "  test           Run pytest suite with volume mounting"
        echo "  image_processor Run image processor with arguments"
        echo "  package        Build and install package locally"
        echo ""
        echo "EXAMPLES:"
        echo "  manage.sh help"
        echo "  manage.sh isession"
        echo "  manage.sh test"
        echo "  manage.sh image_processor images/ --output processed/ --task resize"
        echo "  manage.sh image_processor images/ --output processed/ --task resize --format webp --quality 80"
        exit 0
        ;;
    "isession") cmd_isession ;;
    "test") cmd_run_tests ;;
    "image_processor") cmd_run_image_processor "${_arg_leftovers[@]}" ;;
    "package") cmd_build_package ;;
    *)
        echo "Unknown command: $_arg_command"
        echo "Run 'manage.sh help' for usage"
        exit 1
        ;;
esac
