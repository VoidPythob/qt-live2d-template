#!/usr/bin/env python3
"""配置项目名和 Qt 路径。

写入 CMakeLists.txt 的 APP_NAME，以及 app.env 供其他脚本读取。"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / "app.env"
CMAKE_PATH = ROOT / "CMakeLists.txt"


def load_env() -> dict[str, str]:
    """从 app.env 读取默认值。"""
    defaults: dict[str, str] = {}
    if not ENV_PATH.exists():
        return defaults
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            defaults[k.strip()] = v.strip().strip('"')
    return defaults


def save_env(name: str, qt_path: str) -> None:
    ENV_PATH.write_text(
        f"APP_NAME={name}\nQT_SDK_PATH={qt_path}\n", encoding="utf-8"
    )


def update_cmake(name: str) -> int:
    """替换 CMakeLists.txt 中的 set(APP_NAME ...)，返回替换次数。"""
    text = CMAKE_PATH.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r"set\(APP_NAME\s+\S+\)", f"set(APP_NAME {name})", text
    )
    if n > 0:
        CMAKE_PATH.write_text(new_text, encoding="utf-8")
    return n


def prompt(label: str, default: str | None = None) -> str | None:
    if default:
        label = f"{label} [{default}]: "
    else:
        label = f"{label}: "
    value = input(label).strip()
    return value if value else default


def main() -> int:
    defaults = load_env()

    parser = argparse.ArgumentParser(description="配置项目名和 Qt 路径")
    parser.add_argument("--name", "-n", help="项目名（如 MyLive2DApp）")
    parser.add_argument("--qt-path", "-q", help="Qt SDK 路径（如 D:/Qt/6.11.1/msvc2022_64）")
    args = parser.parse_args()

    name = args.name or prompt("项目名 (APP_NAME)", defaults.get("APP_NAME"))
    qt_path = args.qt_path or prompt("Qt SDK 路径", defaults.get("QT_SDK_PATH"))

    if not name:
        print("错误：项目名不能为空", file=sys.stderr)
        return 1
    if not qt_path:
        print("错误：Qt SDK 路径不能为空", file=sys.stderr)
        return 1

    qt_path = qt_path.replace("\\", "/")

    print(f"\n项目名: {name}")
    print(f"Qt 路径: {qt_path}")
    print()

    n = update_cmake(name)
    if n > 0:
        print(f"  ✓ CMakeLists.txt → set(APP_NAME {name})")
    else:
        print(f"  - CMakeLists.txt (无匹配，跳过)")

    save_env(name, qt_path)
    print(f"  ✓ app.env 已更新")

    print(f"\n完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
