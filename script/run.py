#!/usr/bin/env python3
"""运行 —— 跨平台，替代 run.ps1 / run.sh。

优先从 app.env 读取 APP_NAME，其次从 CMakeLists.txt 解析。"""

import argparse
import os
import platform
import re
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


def get_app_name() -> str:
    """从 app.env 或 CMakeLists.txt 获取 APP_NAME。"""
    app_name = load_env().get("APP_NAME", "")
    if app_name:
        return app_name

    cmake_file = ROOT / "CMakeLists.txt"
    if cmake_file.exists():
        m = re.search(r"set\(APP_NAME\s+(\S+)\)", cmake_file.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    return ""


def main() -> int:
    app_name = get_app_name()
    if not app_name:
        print("错误：未找到 APP_NAME。请先运行 python script/config_app.py", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="运行编译产物")
    parser.add_argument("--config", "-c", default="Release", choices=["Release", "Debug"],
                        help="构建类型")
    args = parser.parse_args()

    system = platform.system()
    build_dir = ROOT / "build"

    exe_name = f"{app_name}.exe" if system == "Windows" else app_name

    # 多配置生成器路径（VS / Xcode），其次单配置路径
    exe_path = build_dir / args.config / exe_name
    if not exe_path.exists():
        exe_path = build_dir / exe_name

    if not exe_path.exists():
        print(f"错误：未找到可执行文件: {exe_path}", file=sys.stderr)
        print("请先运行 python script/cmake.py 和 python script/build.py", file=sys.stderr)
        return 1

    print(f"运行: {exe_path}")
    os.chdir(exe_path.parent)
    return subprocess.run([str(exe_path.name)]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
