param(
    [switch]$ForcePythonInstall
)

$ErrorActionPreference = "Stop"

function Get-UsablePython {
    $candidates = @(
        "$env:LocalAppData\Programs\Python\Python312\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:LocalAppData\Programs\Python\Python313\python.exe",
        "$env:ProgramFiles\Python313\python.exe",
        "python"
    )

    foreach ($candidate in $candidates) {
        try {
            $resolvedPath = (Get-Command $candidate -ErrorAction Stop).Source

            if ($resolvedPath -like "*\WindowsApps\python.exe") {
                continue
            }

            $pythonExecutable = (& $resolvedPath -c "import sys; print(sys.executable)" 2>$null).Trim()
            if ($LASTEXITCODE -eq 0 -and $pythonExecutable) {
                return $resolvedPath
            }
        }
        catch {
        }
    }

    return $null
}

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$pythonCmd = Get-UsablePython

if (-not $pythonCmd -or $ForcePythonInstall) {
    Write-Host "Python 3.12 no esta disponible."
    Write-Host "Instalalo con este comando y vuelve a ejecutar el script:"
    Write-Host "winget install --id Python.Python.3.12 --source winget --accept-package-agreements --accept-source-agreements"
    exit 1
}

Write-Host "Usando Python:" $pythonCmd
& $pythonCmd --version

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    & $pythonCmd -m venv venv
}

$venvPython = ".\venv\Scripts\python.exe"
& $venvPython -m pip install --upgrade pip

if (Test-Path ".\requirements.txt") {
    & $venvPython -m pip install -r .\requirements.txt
}
else {
    & $venvPython -m pip install django djangorestframework psycopg2-binary python-dotenv
}

if (-not (Test-Path ".\.env")) {
    Write-Host "No existe .env en backend/."
    Write-Host "Crea backend/.env manualmente con las variables locales antes de continuar."
    exit 1
}

& $venvPython manage.py migrate

Write-Host ""
Write-Host "Bootstrap completado."
Write-Host "Activa el entorno con: .\venv\Scripts\activate"
Write-Host "Inicia el servidor con: .\venv\Scripts\python.exe manage.py runserver"
