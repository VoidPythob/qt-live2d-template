param(
    [string]$Config = "Release",
    [string]$QtSdkPath = "D:/software/qt/6.11.1/msvc2022_64",
    [switch]$QtProject,
    [switch]$StaticCRT,
    [switch]$UseGLES
)

$BuildDir = "build"

# 清理旧构建
if (Test-Path $BuildDir) {
    Remove-Item -Recurse -Force $BuildDir
}

$CMakeArgs = @(
    "-G", "Visual Studio 17 2022",
    "-A", "x64",
    "-S", ".",
    "-B", $BuildDir,
    "-DCMAKE_PREFIX_PATH=$QtSdkPath",
    "-DQT_SDK_PATH=$QtSdkPath/bin"
)

if ($QtProject) {
    $CMakeArgs += "-DIS_QT_PROJECT=ON"
}

if ($StaticCRT) {
    $CMakeArgs += "-DUSE_STATIC_CRT=ON"
}

if ($UseGLES) {
    $CMakeArgs += "-DUSE_GLES_SHADER=ON"
}

& cmake @CMakeArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "Done. Configured for $Config." -ForegroundColor Green
    Write-Host "Run: cmake --build $BuildDir --config $Config" -ForegroundColor Cyan
} else {
    Write-Host "CMake configuration failed!" -ForegroundColor Red
}