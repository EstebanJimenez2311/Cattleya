# Cattleya - Arquitectura del Sistema

## Backend
- **Framework**: Django 6.0.3 + Django REST Framework
- **Base de datos**: PostgreSQL (con fallback a SQLite)
- **Servidor**: http://127.0.0.1:8000
- **API**: RESTful con endpoints para noticias

## Frontend
- **Archivos**: HTML/CSS/JS vanilla
- **Servidor**: http://127.0.0.1:5500 (Live Server)
- **Conexión**: Directa a API Django (NO serverless)

## Despliegue
- **Netlify**: Solo para archivos estáticos
- **Serverless Functions**: DEPRECATED (marcadas como .deprecated.js)
- **Backend**: Django en servidor dedicado

## Flujo de Datos
1. Django importa RSS automáticamente
2. Frontend consume API REST de Django
3. NO se usan funciones serverless de Netlify

## Configuración CORS
- Django maneja CORS para desarrollo local
- En producción: configurar ALLOWED_HOSTS y CORS_ORIGIN_WHITELIST