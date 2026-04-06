#!/usr/bin/env python
import os
import django
import requests
import json
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from noticias.models import Noticia

# Esperar servidor
time.sleep(2)

print("=" * 80)
print("VALIDACIÓN DE CONSISTENCIA DE DATOS — NIVEL SENIOR")
print("=" * 80)

# ============================================================================
# PASO 1: Datos de verdad (source of truth)
# ============================================================================
print("\n[FUENTE DE VERDAD] Conteos de Noticia.objects")
print("-" * 80)

total_noticias = Noticia.objects.count()
total_verificadas = Noticia.objects.filter(verificada=True).count()

tipos_reales = {
    'fisica': Noticia.objects.filter(violencia_fisica=True).count(),
    'psicologica': Noticia.objects.filter(violencia_psicologica=True).count(),
    'sexual': Noticia.objects.filter(violencia_sexual=True).count(),
    'economica': Noticia.objects.filter(violencia_economica=True).count(),
    'patrimonial': Noticia.objects.filter(violencia_patrimonial=True).count(),
    'feminicidio': Noticia.objects.filter(feminicidio=True).count(),
}

ambitos_reales = {
    'familiar': Noticia.objects.filter(ambito_violencia='familiar').count(),
    'pareja': Noticia.objects.filter(ambito_violencia='pareja').count(),
    'comunitario': Noticia.objects.filter(ambito_violencia='comunitario').count(),
    'institucional': Noticia.objects.filter(ambito_violencia='institucional').count(),
}

print(f"Total noticias: {total_noticias}")
print(f"Total verificadas: {total_verificadas}")
print(f"\nTipos de violencia (DB):")
for tipo, count in tipos_reales.items():
    print(f"  {tipo}: {count}")
print(f"\nÁmbitos (DB):")
for ambito, count in ambitos_reales.items():
    print(f"  {ambito}: {count}")

# ============================================================================
# PASO 2: Obtener datos de API
# ============================================================================
print("\n\n[API] GET /api/estadisticas/resumen/")
print("-" * 80)

response = requests.get('http://localhost:8000/api/estadisticas/resumen/')
if response.status_code == 200:
    api_data = response.json()
    print(f"Status: 200 ✓")
    print(f"Total noticias (API): {api_data['total_noticias']}")
    print(f"Total verificadas (API): {api_data['total_verificadas']}")
    print(f"\nTipos de violencia (API):")
    for tipo, count in api_data['tipos_violencia'].items():
        print(f"  {tipo}: {count}")
    print(f"\nÁmbitos (API):")
    for ambito, count in api_data['ambitos'].items():
        print(f"  {ambito}: {count}")
else:
    print(f"ERROR: {response.status_code}")
    api_data = None

# ============================================================================
# PASO 3: VALIDACIÓN DE CONSISTENCIA
# ============================================================================
print("\n\n[VALIDACIÓN] Comparación DB vs API")
print("=" * 80)

errors = []

# Validar total
if api_data['total_noticias'] != total_noticias:
    errors.append(f"❌ Total noticias: DB={total_noticias}, API={api_data['total_noticias']}")
else:
    print(f"✓ Total noticias: {total_noticias}")

# Validar verificadas
if api_data['total_verificadas'] != total_verificadas:
    errors.append(f"❌ Total verificadas: DB={total_verificadas}, API={api_data['total_verificadas']}")
else:
    print(f"✓ Total verificadas: {total_verificadas}")

# Validar tipos
tipos_api = api_data['tipos_violencia']
for tipo, count_db in tipos_reales.items():
    count_api = tipos_api.get(tipo, 0)
    if count_api != count_db:
        errors.append(f"❌ Tipo {tipo}: DB={count_db}, API={count_api}")
    else:
        print(f"✓ Tipo {tipo}: {count_db}")

# Validar ámbitos
ambitos_api = api_data['ambitos']
for ambito, count_db in ambitos_reales.items():
    count_api = ambitos_api.get(ambito, 0)
    if count_api != count_db:
        errors.append(f"❌ Ámbito {ambito}: DB={count_db}, API={count_api}")
    else:
        print(f"✓ Ámbito {ambito}: {count_db}")

# ============================================================================
# RESULTADO
# ============================================================================
print("\n" + "=" * 80)
if errors:
    print("❌ ENCONTRADOS ERRORES DE INCONSISTENCIA:")
    for error in errors:
        print(f"  {error}")
    print("\n🔥 ESTO SIGNIFICA: Los cálculos de la API NO son confiables")
else:
    print("✅ VALIDACIÓN PASADA — TODOS LOS DATOS SON CONSISTENTES")
    print("\n🎯 La API calcula correctamente en tiempo real")
    print("✓ No hay desincronización de datos")
    print("✓ EstadisticaResumen (caché) podría usarse, pero no es crítico")

print("=" * 80)
