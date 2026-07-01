# Qt Live2D Template

基于 Qt6 + OpenGL 的 Live2D Cubism 渲染模板项目。

## 前置依赖

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| **Qt** | 6.x | Core / Gui / Widgets / OpenGL / OpenGLWidgets |
| **CMake** | ≥ 3.26 | 构建系统 |
| **Visual Studio** | 2022 (MSVC 143+) | Windows 编译工具链 |
| **Live2D Cubism SDK** | — | 已内置在 `Thirdparty/CubismSdk/` |
| **GLFW** | — | 已内置在 `Thirdparty/glfw/`（从源码编译） |
| **GLEW** | — | 已内置在 `Thirdparty/glew/`（从源码编译） |
| **stb** | — | 已内置在 `Thirdparty/stb/` |

> Linux 下使用 GCC/Clang + Unix Makefiles 或 Ninja 构建。

## 项目配置

使用 `config_app.py` 一键配置项目名和 Qt 路径，写入 `CMakeLists.txt` 和 `app.env`：

```bash
# 命令行传参
python script/config_app.py -n MyApp -q D:/Qt/6.11.1/msvc2022_64

# 或交互式输入（已有 app.env 时会显示默认值）
python script/config_app.py
```

配置存储在根目录的 `app.env`，各脚本运行时会自动读取。

## 脚本说明

所有脚本位于 `script/` 目录，跨平台 Python 实现。

### cmake.py — 生成工程

```
python script/cmake.py [-c Release|Debug] [-q Qt路径] [--qt-project] [--static-crt] [--use-gles]
```

| 参数 | 说明 |
|------|------|
| `-c, --config` | 构建类型，默认 `Release` |
| `-q, --qt-path` | Qt SDK 路径（默认从 `app.env` 读取） |
| `--qt-project` | 启用 Qt 模式（链接 Qt6 + windeployqt6） |
| `--static-crt` | 静态链接 MSVC 运行时 (/MT) |
| `--use-gles` | 使用 OpenGL ES 着色器 |

自动按平台选择生成器：Windows → Visual Studio 2022 / macOS → Xcode / Linux → Unix Makefiles。

### build.py — 编译

```
python script/build.py [-c Release|Debug]
```

### run.py — 运行

```
python script/run.py [-c Release|Debug]
```

> APP_NAME 自动从 `app.env` 或 `CMakeLists.txt` 读取。

### config_app.py — 配置

```
python script/config_app.py [-n 项目名] [-q Qt路径]
```

修改内容：
- `CMakeLists.txt` → `set(APP_NAME ...)`
- `app.env` → `APP_NAME` + `QT_SDK_PATH`

## CMake 选项一览

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `CMAKE_PREFIX_PATH` | 脚本默认值 | Qt 安装路径，供 `find_package(Qt6)` 查找 |
| `QT_SDK_PATH` | `""` | windeployqt6 搜索路径（`<QtSdkPath>/bin`） |
| `IS_QT_PROJECT` | `OFF` | 启用后链接 Qt6 库，构建后自动运行 windeployqt6 部署 Qt 依赖 |
| `USE_STATIC_CRT` | `OFF` | 静态链接 MSVC 运行时（/MT），否则动态链接（/MD） |
| `USE_GLES_SHADER` | `OFF` | 使用 OpenGL ES 着色器变体，否则使用桌面 OpenGL 版本 |

## 快速开始（Windows）

```powershell
# 1. 配置（只需执行一次）
python script/config_app.py -n MyApp -q "D:/Qt/6.11.1/msvc2022_64"

# 2. 生成 VS 工程
python script/cmake.py --qt-project

# 3. 编译
python script/build.py -c Release

# 4. 运行
python script/run.py -c Release
```

## 快速开始（Linux）

```bash
# 1. 配置（只需执行一次）
python script/config_app.py -n MyApp -q "/path/to/Qt/6.x/gcc_64"

# 2. 生成 Makefile
python script/cmake.py --qt-project -c Release

# 3. 编译
python script/build.py -c Release

# 4. 运行
python script/run.py -c Release
```

## 项目结构

```
.
├── CMakeLists.txt              # CMake 构建配置
├── app.env                     # 项目配置（由 config_app.py 生成）
├── LAppLive2D/                 # Live2D 应用逻辑层
├── QtLive2dDemo/               # Qt 应用入口（APP_NAME 同名目录）
├── Resources/                  # 模型资源
├── Shaders/                    # 自定义着色器
├── lib/                        # 预编译的 Live2D Cubism Core 库
├── Thirdparty/                 # 第三方库（Cubism SDK / GLFW / GLEW / stb）
└── script/                     # 构建 & 运行脚本（跨平台 Python）
    ├── config_app.py           #   项目配置
    ├── cmake.py                #   生成工程
    ├── build.py                #   编译
    └── run.py                  #   运行
```
