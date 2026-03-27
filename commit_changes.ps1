# Script de PowerShell para hacer commit de todos los cambios pendientes
# Ejecutar desde el directorio raíz del proyecto: c:\Users\Esteban\desktop\cattleya

git add -A

git commit -m "refactor: Corregir arquitectura - eliminar dependencias serverless

- Marcar funciones Netlify como deprecated (.deprecated.js)
- Deshabilitar configuración serverless en netlify.toml
- Actualizar comentarios en frontend para clarificar uso de Django
- Crear ARQUITECTURA.md explicando el flujo Django + frontend
- Frontend ahora usa exclusivamente API REST de Django"