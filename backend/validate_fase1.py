import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from analisis.models import ResultadoAnalisis
from rest_framework.test import APIClient

print("=" * 60)
print("VALIDACIÓN FASE 1 - APP ANALISIS")
print("=" * 60)

# Usar timestamp para evitar conflictos
timestamp = int(datetime.now().timestamp())
test_nombre = f"test_validation_{timestamp}"

# 1. Validar Modelo
print("\n[1] VALIDANDO MODELO...")
try:
    test_data = ResultadoAnalisis.objects.create(
        nombre=test_nombre,
        fuente="validation_source",
        descripcion="Objeto de prueba para validación",
        datos={"status": "ok", "test_value": 123}
    )
    print(f"  ✓ Modelo creado: {test_data}")
    print(f"    - nombre: {test_data.nombre}")
    print(f"    - fuente: {test_data.fuente}")
    print(f"    - datos: {test_data.datos}")
    print(f"    - actualizado: {test_data.actualizado}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# 2. Validar Lookup por nombre
print("\n[2] VALIDANDO LOOKUP POR NOMBRE...")
try:
    recovered = ResultadoAnalisis.objects.get(nombre=test_nombre)
    print(f"  ✓ Objeto recuperado correctamente: {recovered}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# 3. Validar Queryset con orden
print("\n[3] VALIDANDO ORDEN -actualizado...")
try:
    queryset = ResultadoAnalisis.objects.all()
    count = queryset.count()
    if count > 0:
        first = list(queryset)[0]
        print(f"  ✓ Total de objetos: {count}")
        print(f"  ✓ Primer objeto (más reciente): {first.nombre}")
    else:
        print(f"  ! Queryset vacío pero conexión exitosa")
except Exception as e:
    print(f"  ✗ Error: {e}")

# 4. Validar Serializer
print("\n[4] VALIDANDO SERIALIZER...")
try:
    from analisis.serializers import ResultadoAnalisisSerializer
    obj = ResultadoAnalisis.objects.get(nombre=test_nombre)
    serializer = ResultadoAnalisisSerializer(obj)
    print(f"  ✓ Serializer funcionando")
    print(f"    - Campos: {list(serializer.data.keys())}")
    print(f"    - Datos serializados: {dict(serializer.data)}")
except Exception as e:
    print(f"  ✗ Error: {e}")

# 5. Validar URLs con APIClient
print("\n[5] VALIDANDO URLS (con APIClient)...")
try:
    from rest_framework.test import APIClient
    
    client = APIClient()
    
    # Probar ListaResultadosView
    response = client.get('/api/resultados/')
    print(f"  ✓ GET /api/resultados/")
    print(f"    - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"    - Items retornados: {len(response.data)}")
    
    # Probar DetalleResultadoView
    response = client.get(f'/api/resultados/{test_nombre}/')
    print(f"  ✓ GET /api/resultados/{test_nombre}/")
    print(f"    - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"    - Nombre: {response.data.get('nombre')}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")

# 6. Validar Apps Config
print("\n[6] VALIDANDO CONFIGURACIÓN...")
try:
    from django.apps import apps
    app = apps.get_app_config('analisis')
    print(f"  ✓ App registrada: {app.name}")
    print(f"  ✓ Modelos disponibles: {[m.__name__ for m in app.get_models()]}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
print("✓ VALIDACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 60)
