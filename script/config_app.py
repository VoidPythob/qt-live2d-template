#!/usr/bin/env python3
"""配置项目名和 Qt 路径，写入 CMakeLists.txt 和各平台脚本。"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = {
    "cmakelists": {
        "path": ROOT / "CMakeLists.txt",
        "replacements": [
            # set(APP_NAME <name>)
            (r"set\(APP_NAME\s+\S+\)", 'set(APP_NAME {name})'),
        ],
    },
    "cmake_ps1": {
        "path": ROOT / "script" / "win" / "cmake.ps1",
        "replacements": [
            # $QtSdkPath = "..."
            (r'\$QtSdkPath\s*=\s*"[^"]*"', '$QtSdkPath = "{qt_path}"'),
        ],
    },
    "run_ps1": {
        "path": ROOT / "script" / "win" / "run.ps1",
        "replacements": [
            # $AppName = "..."
            (r'\$AppName\s*=\s*"[^"]*"', '$AppName = "{name}"'),
        ],
    },
    "cmake_sh": {
        "path": ROOT / "script" / "linux" / "cmake.sh",
        "replacements": [
            # QT_SDK_PATH="..." （仅变量赋值行，排除 -DQT_SDK_PATH= 的 cmake 参数行）
            (r'(?<!-D)QT_SDK_PATH="[^"]*"', 'QT_SDK_PATH="{qt_path}"'),
        ],
    },
    "run_sh": {
        "path": ROOT / "script" / "linux" / "run.sh",
        "replacements": [
            # APP_NAME="..."
            (r'APP_NAME="[^"]*"', 'APP_NAME="{name}"'),
        ],
    },
}


def apply(filepath: Path, replacements: list[tuple[str, str]], name: str, qt_path: str) -> int:
    """对单个文件应用所有替换，返回替换次数。"""
    text = filepath.read_text(encoding="utf-8")
    count = 0
    for pattern, template in replacements:
        new_text, n = re.subn(pattern, template.format(name=name, qt_path=qt_path), text)
        if n > 0:
            count += n
            text = new_text
    if count > 0:
        filepath.write_text(text, encoding="utf-8")
    return count


def main():
    parser = argparse.ArgumentParser(description="配置 Qt Live2D 项目名和 Qt 路径")
    parser.add_argument("--name", "-n", help="项目名（如 MyLive2DApp）")
    parser.add_argument("--qt-path", "-q", help="Qt SDK 路径（如 D:/Qt/6.11.1/msvc2022_64）")
    args = parser.parse_args()

    # 交互式输入
    name = args.name or input("项目名 (APP_NAME): ").strip()
    qt_path = args.qt_path or input("Qt SDK 路径: ").strip()

    if not name:
        print("错误：项目名不能为空")
        return 1
    if not qt_path:
        print("错误：Qt SDK 路径不能为空")
        return 1

    # 规范化路径分隔符
    qt_path = qt_path.replace("\\", "/")

    print(f"\n项目名: {name}")
    print(f"Qt 路径: {qt_path}")
    print()

    total = 0
    for key, cfg in FILES.items():
        n = apply(cfg["path"], cfg["replacements"], name, qt_path)
        if n > 0:
            print(f"  ✓ {cfg['path'].relative_to(ROOT)} ({n} 处)")
            total += n
        else:
            print(f"  - {cfg['path'].relative_to(ROOT)} (无匹配，跳过)")

    print(f"\n完成，共修改 {total} 处。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
