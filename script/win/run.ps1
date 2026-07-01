param(
    [string]$Config = "Release"
)

$BuildDir = "build"
$AppName = "QtLive2dDemo"
$ExePath = "$BuildDir\$Config\$AppName.exe"

if (-not (Test-Path $ExePath)) {
    # 尝试单配置生成器路径（Ninja/NMake）
    $ExePath = "$BuildDir\$AppName.exe"
    if (-not (Test-Path $ExePath)) {
        Write-Error "Executable not found: $ExePath"
        Write-Host "Run .\script\cmake.ps1 and .\script\build.ps1 first." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "Running: $ExePath" -ForegroundColor Cyan
Push-Location (Split-Path $ExePath -Parent)
try {
    & ".\$AppName.exe"
} finally {
    Pop-Location
}
