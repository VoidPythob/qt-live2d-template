cmake_minimum_required(VERSION 3.26)

set(APP_NAME ciallo)
project(${APP_NAME})

# 第三方库根目录
set(THIRDPARTY_DIR ${CMAKE_SOURCE_DIR}/Thirdparty)

# 设定cmake选项
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# 设定渲染框架为 opengl
set(FRAMEWORK_SOURCE OpenGL)
set(FRAMEWORK_DEFINITIOINS -DCSM_TARGET_WIN_GL)

# GLFW 从源码编译
set(GLFW_INSTALL OFF CACHE BOOL "" FORCE)
add_subdirectory(${THIRDPARTY_DIR}/glfw)

# GLEW 从源码编译（静态库）
add_library(libglew STATIC
    ${THIRDPARTY_DIR}/glew/src/glew.c
)
target_include_directories(libglew PUBLIC ${THIRDPARTY_DIR}/glew/include)
target_compile_definitions(libglew PUBLIC GLEW_STATIC)
# 确保生成调试信息，避免 LNK4204 警告
target_compile_options(libglew PRIVATE $<$<C_COMPILER_ID:MSVC>:/Zi>)
# 抑制 glew.h 与 Windows SDK 的 APIENTRY 宏重定义警告
target_compile_options(libglew PRIVATE $<$<C_COMPILER_ID:MSVC>:/wd4005>)

# TODO 将来可能删除此FLAG
option(IS_QT_PROJECT "Qt Project Flag, Test Not Qt Project, Will Delete" OFF)
# Qt开发工具链位置
option(QT_SDK_PATH "Qt Sdk Path" "")
# CRT 链接方式选项：MT（静态CRT）/ MD（动态CRT）
option(USE_STATIC_CRT "Use static CRT (/MT) instead of dynamic CRT (/MD)" OFF)

# Cubism 着色器变体选项：Standard（桌面OpenGL）/ StandardES（OpenGL ES）
option(USE_GLES_SHADER "Use OpenGL ES shader variant (StandardES) instead of Standard" OFF)

if(USE_STATIC_CRT)
    set(CUBISM_CRT_SUFFIX "MT")
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
else()
    set(CUBISM_CRT_SUFFIX "MD")
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()

set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT ${APP_NAME})

file(GLOB LappLive "LAppLive2D/*.cpp")

# 添加qt库
find_package(Qt6 COMPONENTS
    Core
    Gui
    Widgets
    OpenGL
    OpenGLWidgets
    REQUIRED
)

# 头文件搜索路径
include_directories(./
    LAppLive2D
    ${THIRDPARTY_DIR}/CubismSdk/Core/include

    ${THIRDPARTY_DIR}/CubismSdk/Framework/src
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Effect
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Id
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Math
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Model
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Motion
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Physics
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Rendering
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Type
    ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Utils

    ${THIRDPARTY_DIR}/glew/include
    ${THIRDPARTY_DIR}/glfw/include

    ${THIRDPARTY_DIR}/stb
)

add_executable(${APP_NAME}
    ${APP_NAME}/src/main.cpp
    "${LappLive}"
)

# 添加opengl宏定义
target_compile_definitions(${APP_NAME} PRIVATE CSM_TARGET_WIN_GL)

add_subdirectory(${THIRDPARTY_DIR}/CubismSdk/Framework)

target_compile_definitions(Framework PRIVATE GLEW_STATIC)

# 根据平台/架构确定 Cubism Core 库路径
if(WIN32)
    set(CUBISM_PLATFORM windows)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(CUBISM_ARCH x86_64)
    else()
        set(CUBISM_ARCH x86)
    endif()
    if(MSVC_VERSION GREATER_EQUAL 1930)
        set(CUBISM_MSVC_VER 143)
    elseif(MSVC_VERSION GREATER_EQUAL 1920)
        set(CUBISM_MSVC_VER 142)
    else()
        set(CUBISM_MSVC_VER 141)
    endif()
    set(CUBISM_CORE_DIR ${CMAKE_SOURCE_DIR}/lib/${CUBISM_PLATFORM}/${CUBISM_ARCH}/${CUBISM_MSVC_VER})
    set(CUBISM_CORE_LIB Live2DCubismCore_${CUBISM_CRT_SUFFIX}$<$<CONFIG:Debug>:d>)
elseif(APPLE)
    set(CUBISM_PLATFORM macos)
    if(CMAKE_SYSTEM_PROCESSOR MATCHES "arm64|aarch64")
        set(CUBISM_ARCH arm64)
    else()
        set(CUBISM_ARCH x86_64)
    endif()
    set(CUBISM_CORE_DIR ${CMAKE_SOURCE_DIR}/lib/${CUBISM_PLATFORM}/${CUBISM_ARCH})
    set(CUBISM_CORE_LIB Live2DCubismCore)
else()
    set(CUBISM_PLATFORM linux)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(CUBISM_ARCH x86_64)
    else()
        set(CUBISM_ARCH x86)
    endif()
    set(CUBISM_CORE_DIR ${CMAKE_SOURCE_DIR}/lib/${CUBISM_PLATFORM}/${CUBISM_ARCH})
    set(CUBISM_CORE_LIB Live2DCubismCore)
endif()

# 添加库文件搜索路径
target_link_directories(${APP_NAME} PRIVATE ${CUBISM_CORE_DIR})

target_link_libraries(${APP_NAME}
    Framework
    ${CUBISM_CORE_LIB}
    libglew
    glfw
    opengl32
    glu32
)

if(IS_QT_PROJECT)
    target_link_libraries(${APP_NAME}
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
        Qt6::OpenGL
        Qt6::OpenGLWidgets
    )
endif()


if (IS_QT_PROJECT)
    # 部署qt依赖
    find_program(WINDEPLOYQT6 windeployqt6
        PATHS ${QT_SDK_PATH}
    )
    add_custom_command(TARGET ${APP_NAME} POST_BUILD
        COMMAND ${WINDEPLOYQT6}
            --dir $<TARGET_FILE_DIR:${APP_NAME}>
            $<TARGET_FILE:${APP_NAME}>
        COMMENT "Deploying Qt dependencies..."
    )
else()
    message("Not Qt Project, Not Need Deploying Qt")
endif()


# 部署资源
add_custom_command(TARGET ${APP_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/Resources
        $<TARGET_FILE_DIR:${APP_NAME}>/Resources
    COMMENT "Deploying Resources..."
)

# 根据选项选择着色器变体
if(USE_GLES_SHADER)
    set(CUBISM_SHADER_DIR ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Rendering/OpenGL/Shaders/StandardES)
    set(SAMPLE_SHADER_DIR ${CMAKE_SOURCE_DIR}/Shaders/StandardES)
else()
    set(CUBISM_SHADER_DIR ${THIRDPARTY_DIR}/CubismSdk/Framework/src/Rendering/OpenGL/Shaders/Standard)
    set(SAMPLE_SHADER_DIR ${CMAKE_SOURCE_DIR}/Shaders/Standard)
endif()

# 部署着色器
add_custom_command(TARGET ${APP_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${SAMPLE_SHADER_DIR}
        $<TARGET_FILE_DIR:${APP_NAME}>/SampleShaders
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CUBISM_SHADER_DIR}
        $<TARGET_FILE_DIR:${APP_NAME}>/FrameworkShaders
    COMMENT "Deploying Shaders..."
)