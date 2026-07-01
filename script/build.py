#!/usr/bin/env python3
"""编译 —— 跨平台，替代 build.ps1 / build.sh。"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="编译项目")
    parser.add_argument("--config", "-c", default="Release", choices=["Release", "Debug"],
                        help="构建类型")
    args = parser.parse_args()

    build_dir = ROOT / "build"
    if not (build_dir / "CMakeCache.txt").exists():
        print("错误：未找到 CMakeCache.txt，请先运行 python script/cmake.py", file=sys.stderr)
        return 1

    cmd = ["cmake", "--build", str(build_dir), "--config", args.config]
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"完成。输出: build/{args.config}/")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
