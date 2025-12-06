# Panopt Lite - Windows Agent Launcher
# This script downloads Vector (Log Collector) and runs it with the local config.

$VectorVersion = "0.41.0"
$VectorUrl = "https://packages.timber.io/vector/${VectorVersion}/vector-${VectorVersion}-x86_64-pc-windows-msvc.zip"
$InstallDir = "$PSScriptRoot\bin"

# 1. Create Bin Directory
if (-not (Test-Path $InstallDir)) {
    Write-Host "Creating install directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

# 2. Download Vector if not present
if (-not (Get-ChildItem -Path $InstallDir -Filter vector.exe -Recurse -ErrorAction SilentlyContinue)) {
    Write-Host "Downloading Vector ${VectorVersion}..." -ForegroundColor Cyan
    $ZipPath = "$InstallDir\vector.zip"
    Invoke-WebRequest -Uri $VectorUrl -OutFile $ZipPath
    
    Write-Host "Extracting Vector..." -ForegroundColor Cyan
    Expand-Archive -Path $ZipPath -DestinationPath $InstallDir -Force
    Remove-Item $ZipPath
}

# 3. Find Vector Executable
$VectorExe = (Get-ChildItem -Path $InstallDir -Filter vector.exe -Recurse | Select-Object -First 1).FullName

# 3. Run Vector
Write-Host "Starting Vector Agent..." -ForegroundColor Green
Write-Host "Forwarding Windows Event Logs to Loki (localhost:3100)..." -ForegroundColor Gray
Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow

& $VectorExe --config "$PSScriptRoot\vector-windows.toml"
