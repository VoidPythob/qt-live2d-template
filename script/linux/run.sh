#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-Release}"
BUILD_DIR="build"
APP_NAME="QtLive2dDemo"

# 查找可执行文件
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    EXE_PATH="$BUILD_DIR/$APP_NAME"
    if [[ ! -f "$EXE_PATH" ]]; then
        # 尝试 Xcode 多配置路径
        EXE_PATH="$BUILD_DIR/$CONFIG/$APP_NAME"
    fi
else
    # Linux
    EXE_PATH="$BUILD_DIR/$APP_NAME"
    if [[ ! -f "$EXE_PATH" ]]; then
        # 尝试多配置生成器路径
        EXE_PATH="$BUILD_DIR/$CONFIG/$APP_NAME"
    fi
fi

if [[ ! -f "$EXE_PATH" ]]; then
    echo "Error: Executable not found: $EXE_PATH" >&2
    echo "Run ./script/cmake.sh and ./script/build.sh first." >&2
    exit 1
fi

echo "Running: $EXE_PATH"
cd "$(dirname "$EXE_PATH")"
./"$APP_NAME"
