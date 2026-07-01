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

使用 `config_app.py` 一键配置项目名和 Qt 路径，会自动写入 CMakeLists.txt 和各平台脚本。

```bash
# 命令行传参
python script/config_app.py -n MyLive2DApp -q D:/Qt/6.11.1/msvc2022_64

# 或交互式输入
python script/config_app.py
```

脚本会修改以下文件：

| 文件 | 配置项 |
|------|--------|
| `CMakeLists.txt` | `set(APP_NAME ...)` |
| `script/win/cmake.ps1` | `$QtSdkPath` |
| `script/win/run.ps1` | `$AppName` |
| `script/linux/cmake.sh` | `QT_SDK_PATH` |
| `script/linux/run.sh` | `APP_NAME` |

也可以手动传参覆盖脚本默认值，见下方脚本说明。

## 脚本说明

所有脚本位于 `script/` 目录下，分 Windows（PowerShell）和 Linux（bash）两套。

### Windows

| 脚本 | 用途 | 参数 |
|------|------|------|
| [cmake.ps1](script/win/cmake.ps1) | 生成 VS 工程，清理旧构建目录 | `-Config` Release/Debug<br>`-QtSdkPath` Qt 安装路径<br>`-QtProject` 启用 Qt 模式<br>`-StaticCRT` 静态链接 CRT<br>`-UseGLES` 使用 OpenGL ES 着色器 |
| [build.ps1](script/win/build.ps1) | 编译项目（需先执行 cmake.ps1） | `-Config` Release/Debug |
| [run.ps1](script/win/run.ps1) | 运行编译产物 | `-Config` Release/Debug |

### Linux

| 脚本 | 用途 | 参数 |
|------|------|------|
| [cmake.sh](script/linux/cmake.sh) | 生成 Makefile，清理旧构建 | `Release` 或 `Debug`（第一个位置参数）<br>`--qt-project` 启用 Qt 模式<br>`--static-crt` 静态链接 CRT<br>`--use-gles` 使用 OpenGL ES 着色器 |
| [build.sh](script/linux/build.sh) | 编译项目（需先执行 cmake.sh） | `Release` 或 `Debug`（第一个位置参数） |
| [run.sh](script/linux/run.sh) | 运行编译产物 | `Release` 或 `Debug`（第一个位置参数） |

### CMake 选项一览

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
.\script\win\cmake.ps1 -QtProject

# 3. 编译
.\script\win\build.ps1 -Config Release

# 4. 运行
.\script\win\run.ps1 -Config Release
```

## 快速开始（Linux）

```bash
# 1. 配置（只需执行一次）
python script/config_app.py -n MyApp -q "/path/to/Qt/6.x/gcc_64"

# 2. 生成 Makefile
./script/linux/cmake.sh Release --qt-project

# 3. 编译
./script/linux/build.sh Release

# 4. 运行
./script/linux/run.sh Release
```

## 项目结构

```
.
├── CMakeLists.txt              # CMake 构建配置
├── README.md
├── LAppLive2D/                 # Live2D 应用逻辑层
├── QtLive2dDemo/               # Qt 应用入口（APP_NAME 同名目录）
├── Resources/                  # 模型资源
├── Shaders/                    # 自定义着色器
│   ├── Standard/               #   桌面 OpenGL 变体
│   └── StandardES/             #   OpenGL ES 变体
├── lib/                        # 预编译的 Live2D Cubism Core 库
├── Thirdparty/                 # 第三方库（Cubism SDK / GLFW / GLEW / stb）
└── script/                     # 构建 & 运行脚本
    ├── config_app.py           #   项目配置脚本（项目名 / Qt 路径）
    ├── win/                    #   Windows PowerShell 脚本
    └── linux/                  #   Linux bash 脚本
```
