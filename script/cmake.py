#!/usr/bin/env python3
"""CMake 配置 —— 跨平台，替代 cmake.ps1 / cmake.sh。

从 app.env 读取 QT_SDK_PATH 默认值。"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    env_path = ROOT / "app.env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"')
    return env


def main() -> int:
    defaults = load_env()

    parser = argparse.ArgumentParser(description="配置 CMake 工程")
    parser.add_argument("--config", "-c", default="Release", choices=["Release", "Debug"],
                        help="构建类型")
    parser.add_argument("--qt-path", "-q", default=defaults.get("QT_SDK_PATH", ""),
                        help="Qt SDK 路径")
    parser.add_argument("--qt-project", action="store_true",
                        help="启用 Qt 模式（链接 Qt6 + windeployqt6）")
    parser.add_argument("--static-crt", action="store_true",
                        help="静态链接 MSVC 运行时 (/MT)")
    parser.add_argument("--use-gles", action="store_true",
                        help="使用 OpenGL ES 着色器")
    args = parser.parse_args()

    if not args.qt_path:
        print("错误：未设置 Qt SDK 路径。用 --qt-path 指定，或先运行 config_app.py 生成 app.env")
        return 1

    build_dir = ROOT / "build"

    # 清理旧构建
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # 按平台选择生成器
    system = platform.system()
    if system == "Windows":
        generator = "Visual Studio 17 2022"
        gen_args = ["-A", "x64"]
    elif system == "Darwin":
        generator = "Xcode"
        gen_args = []
    else:
        generator = "Unix Makefiles"
        gen_args = []

    cmd = [
        "cmake", "-G", generator,
        *gen_args,
        "-S", str(ROOT),
        "-B", str(build_dir),
        f"-DCMAKE_PREFIX_PATH={args.qt_path}",
        f"-DQT_SDK_PATH={args.qt_path}/bin",
    ]

    # 单配置生成器需要 CMAKE_BUILD_TYPE，多配置生成器（VS/Xcode）不需要
    if system not in ("Windows", "Darwin"):
        cmd.append(f"-DCMAKE_BUILD_TYPE={args.config}")

    if args.qt_project:
        cmd.append("-DIS_QT_PROJECT=ON")
    if args.static_crt:
        cmd.append("-DUSE_STATIC_CRT=ON")
    if args.use_gles:
        cmd.append("-DUSE_GLES_SHADER=ON")

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"完成。已配置为 {args.config}。")
        print(f"下一步: python script/build.py --config {args.config}")
    else:
        print("CMake 配置失败！", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
