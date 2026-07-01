#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-Release}"
BUILD_DIR="build"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# ---- 可配置项（由 config_app.py 写入）----
QT_SDK_PATH="D:/software/qt/6.11.1/msvc2022_64"
# -----------------------------------------

QT_PROJECT="OFF"
STATIC_CRT="OFF"
USE_GLES="OFF"

# 解析命名参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --qt-project)   QT_PROJECT="ON"; shift ;;
        --static-crt)   STATIC_CRT="ON"; shift ;;
        --use-gles)     USE_GLES="ON"; shift ;;
        *)              shift ;;
    esac
done

# 清理旧构建
rm -rf "$PROJECT_DIR/$BUILD_DIR"

cmake \
    -G "Unix Makefiles" \
    -S "$PROJECT_DIR" \
    -B "$PROJECT_DIR/$BUILD_DIR" \
    -DCMAKE_BUILD_TYPE="$CONFIG" \
    -DCMAKE_PREFIX_PATH="$QT_SDK_PATH" \
    -DQT_SDK_PATH="$QT_SDK_PATH/bin" \
    -DIS_QT_PROJECT="$QT_PROJECT" \
    -DUSE_STATIC_CRT="$STATIC_CRT" \
    -DUSE_GLES_SHADER="$USE_GLES"

if [[ $? -eq 0 ]]; then
    echo "Done. Configured for $CONFIG."
    echo "Run: cmake --build $BUILD_DIR --config $CONFIG"
else
    echo "CMake configuration failed!" >&2
    exit 1
fi
