# Despliegue de CATTLEYA

Este proyecto se despliega mejor separando:

- `backend/` en Render como servicio web Python + base de datos PostgreSQL.
- `cattleya-sitio/` en Netlify como sitio estatico.

## Arquitectura recomendada

- Backend publico: `https://TU-BACKEND.onrender.com`
- Frontend publico: `https://TU-SITIO.netlify.app`
- API principal usada por el frontend: `https://TU-BACKEND.onrender.com/api/noticias/recientes/`

## 1. Desplegar el backend en Render

Render puede leer [render.yaml](/c:/Users/Esteban/desktop/cattleya/render.yaml), pero antes de crear el servicio revisa estos valores:

- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_CORS_ALLOWED_ORIGINS`

Por defecto el archivo tiene dominios ejemplo:

- `cattleya-backend.onrender.com`
- `cattleya.netlify.app`

Reemplazalos por los dominios reales que te asigne Render y Netlify.

### Variables necesarias del backend

Ademas de las que ya define `render.yaml`, configura o verifica:

- `DJANGO_SECRET_KEY`: una clave nueva y segura para produccion.
- `DJANGO_DEBUG=False`
- `DB_ENGINE=postgres`
- `POSTGRES_SSLMODE=require`

### Flujo sugerido en Render

1. Conecta el repositorio.
2. Crea un nuevo Blueprint y deja que Render lea [render.yaml](/c:/Users/Esteban/desktop/cattleya/render.yaml).
3. Espera a que cree:
   - un servicio web `cattleya-backend`
   - una base de datos `cattleya-db`
4. En el servicio web, agrega `DJANGO_SECRET_KEY`.
5. Corrige `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS` y `DJANGO_CORS_ALLOWED_ORIGINS` con tus dominios reales.
6. Despliega.

### Verificacion del backend

Cuando Render termine, valida:

- `https://TU-BACKEND.onrender.com/health/`
- `https://TU-BACKEND.onrender.com/api/noticias/`
- `https://TU-BACKEND.onrender.com/api/noticias/recientes/`
- `https://TU-BACKEND.onrender.com/admin/`

## 2. Configurar el frontend para apuntar al backend real

El frontend ahora usa [config.js](/c:/Users/Esteban/desktop/cattleya/cattleya-sitio/js/config.js) para definir la URL de la API.

Antes de desplegar el frontend, edita ese archivo:

```js
window.CATTLEYA_CONFIG = window.CATTLEYA_CONFIG || {
  API_BASE_URL: "https://TU-BACKEND.onrender.com"
};
```

En desarrollo local puedes dejarlo vacio y el sitio seguira usando `http://127.0.0.1:8000`.

## 3. Desplegar el frontend en Netlify

El archivo [netlify.toml](/c:/Users/Esteban/desktop/cattleya/netlify.toml) ya publica desde `cattleya-sitio/`.

### Flujo sugerido en Netlify

1. Crea un nuevo sitio desde el repositorio.
2. Usa estas opciones:
   - Base directory: vacio
   - Build command: vacio
   - Publish directory: `cattleya-sitio`
3. Despliega.
4. Toma la URL final de Netlify.
5. Regresa a Render y actualiza `DJANGO_CORS_ALLOWED_ORIGINS` y `DJANGO_CSRF_TRUSTED_ORIGINS` si hace falta.
6. Vuelve a desplegar el backend.

## 4. Orden recomendado para dejar la demo lista

1. Ajusta dominios ejemplo en [render.yaml](/c:/Users/Esteban/desktop/cattleya/render.yaml).
2. Despliega backend en Render.
3. Copia la URL real del backend en [config.js](/c:/Users/Esteban/desktop/cattleya/cattleya-sitio/js/config.js).
4. Despliega frontend en Netlify.
5. Actualiza CORS del backend con la URL real de Netlify.
6. Verifica la pagina de testimonios, que es la que consume noticias dinamicas.

## 5. Checklist ejecutivo

- `healthcheck` responde `ok`
- API publica accesible
- Admin abre correctamente
- Frontend carga
- Pagina `testimonios.html` muestra noticias reales
- CORS habilitado solo para el dominio del frontend
- `DJANGO_SECRET_KEY` rotada para produccion

## 6. Riesgos a tener presentes

- El archivo `backend/.env` local contiene credenciales de desarrollo. No debe reutilizarse tal cual en produccion.
- Si cambian los dominios finales, debes actualizar `render.yaml` y `cattleya-sitio/js/config.js`.
- Si quieres un despliegue mas portable a futuro, el siguiente paso natural seria mover la configuracion del frontend a una inyeccion de entorno en build, pero para la demo actual `config.js` es suficiente y simple.
