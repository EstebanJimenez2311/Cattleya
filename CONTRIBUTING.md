# CONTRIBUTING

## Levantar el proyecto

1. Ir a la carpeta del backend:

```bash
cd backend
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:

```bash
python manage.py migrate
```

4. Crear superusuario:

```bash
python manage.py createsuperuser
```

5. Iniciar el servidor:

```bash
python manage.py runserver
```

6. Abrir el frontend desde `cattleya-sitio/` con un servidor estático o Live Server.

## Convenciones de código

- El backend es Django + DRF. Mantén la lógica de negocio en modelos, servicios y vistas de API.
- El frontend es HTML/CSS/JS vanilla. Evita agregar frameworks nuevos sin necesidad.
- Las URLs del frontend apuntan a `http://127.0.0.1:8000` para el backend.
- Los componentes personalizados se encuentran en `cattleya-sitio/assets/components/`.

## Cómo añadir endpoints

1. Crear o extender una app existente (`noticias`, `analisis`, `estadisticas`).
2. Definir la lógica de la vista en `views.py`.
3. Crear el serializer correspondiente si el endpoint devuelve datos JSON.
4. Registrar la ruta en `urls.py` de la app.
5. Confirmar el endpoint en `backend/config/urls.py` si es una ruta de API principal.
6. Probar con `curl`, Postman o el navegador.

## Cómo trabajar con datos

- `Noticia` es el modelo central y aplica clasificación automática en `save()`.
- Para nuevas métricas en `estadisticas`, agrega lógica en las vistas y serializers.
- Para análisis offline, usa `ResultadoAnalisis` con el campo `datos` para JSON flexible.

## Buenas prácticas

- No modificar `cattleya-sitio/netlify/functions/noticias-proxy.js` como parte del pipeline principal. Esta función es deprecada.
- Separar claramente:
  - ingestión de noticias (`backend/noticias/services`)
  - análisis y resultados (`backend/analisis`)
  - métricas dinámicas (`backend/estadisticas`)
- Mantener el admin ligero y solo exponer operaciones necesarias.

## Ejemplos de Git flow

- Branch para features: `feature/<nombre-funcionalidad>`.
- Branch para fixes: `fix/<problema>`.
- Mensajes de commit claros: `feat: agregar endpoint de tendencias`, `fix: corregir serializador duplicado`.

## Nota de contribución

Si agregas un comando de administración nuevo, regístralo bajo `backend/noticias/management/commands/` o en la app que corresponda, y documenta su uso en este archivo.
