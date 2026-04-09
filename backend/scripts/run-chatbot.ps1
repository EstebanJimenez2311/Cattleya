$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "No existe el entorno virtual. Ejecuta primero .\scripts\bootstrap.ps1"
    exit 1
}

& ".\venv\Scripts\python.exe" ".\files\app.py"
