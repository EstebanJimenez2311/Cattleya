$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "No existe el entorno virtual. Ejecuta primero .\scripts\bootstrap.ps1"
    exit 1
}

if (-not (Test-Path ".\.env")) {
    Write-Host "No existe .env. Crea el archivo desde .env.example y completa las credenciales."
    exit 1
}

$env:DJANGO_SETTINGS_MODULE = "config.settings"
$envVars = Get-Content ".\.env" | Where-Object { $_ -match "=" -and -not $_.StartsWith("#") }
foreach ($line in $envVars) {
    $parts = $line -split "=", 2
    if ($parts.Length -eq 2) {
        [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1], "Process")
    }
}

& ".\venv\Scripts\python.exe" manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); username = __import__('os').environ.get('DJANGO_SUPERUSER_USERNAME'); email = __import__('os').environ.get('DJANGO_SUPERUSER_EMAIL'); password = __import__('os').environ.get('DJANGO_SUPERUSER_PASSWORD'); assert username and email and password, 'Faltan variables DJANGO_SUPERUSER_* en .env'; user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True}); user.email = email; user.is_staff = True; user.is_superuser = True; user.set_password(password); user.save(); print('Superusuario listo:', username)"
