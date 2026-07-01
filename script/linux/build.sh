#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-Release}"
BUILD_DIR="build"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [[ ! -f "$PROJECT_DIR/$BUILD_DIR/CMakeCache.txt" ]]; then
    echo "Error: No CMake cache found. Run ./script/cmake.sh first." >&2
    exit 1
fi

cmake --build "$PROJECT_DIR/$BUILD_DIR" --config "$CONFIG"

echo "Done. Output: $BUILD_DIR/" >&2
