param(
    [string]$Config = "Release"
)

$BuildDir = "build"

if (-not (Test-Path "$BuildDir/CMakeCache.txt")) {
    Write-Error "No CMake cache found. Run ./cmake.ps1 first."
    exit 1
}

& cmake --build $BuildDir --config $Config

Write-Host "Done. Output: build/$Config/" -ForegroundColor Green
