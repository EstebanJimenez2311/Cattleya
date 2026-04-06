import requests
import json
import time

# Esperar a que servidor esté listo
time.sleep(1)

print("=" * 80)
print("VALIDACIÓN COMPLETA FASE 1 - ENDPOINTS EN VIVO")
print("=" * 80)

base_url = "http://localhost:8000"

endpoints = [
    ("/api/analisis/resultados/", "Lista de resultados de análisis"),
    ("/api/estadisticas/resumen/", "Resumen de estadísticas"),
    ("/api/estadisticas/tendencia/", "Tendencia mensual"),
    ("/api/estadisticas/tipos/", "Conteo de tipos de violencia"),
]

results = {}

# ============================================================================
# TEST 1: /api/analisis/resultados/
# ============================================================================
print("\n[1] GET /api/analisis/resultados/")
print("-" * 80)
try:
    response = requests.get(f"{base_url}/api/analisis/resultados/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ PASS - Retorna {len(data)} resultados")
        if data:
            print(f"Estructura del primer resultado:")
            print(json.dumps(data[0], indent=2, ensure_ascii=False))
        results['analisis_lista'] = 'PASS'
    else:
        print(f"✗ FAIL - Status {response.status_code}")
        results['analisis_lista'] = 'FAIL'
except Exception as e:
    print(f"✗ ERROR - {e}")
    results['analisis_lista'] = 'ERROR'

# ============================================================================
# TEST 2: /api/analisis/resultados/{nombre}/
# ============================================================================
print("\n\n[2] GET /api/analisis/resultados/<nombre>/")
print("-" * 80)
try:
    # Obtener el primer resultado
    response = requests.get(f"{base_url}/api/analisis/resultados/")
    if response.status_code == 200 and response.json():
        nombre_test = response.json()[0]['nombre']
        response = requests.get(f"{base_url}/api/analisis/resultados/{nombre_test}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ PASS - Detalle obtenido para: {nombre_test}")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            results['analisis_detalle'] = 'PASS'
        else:
            print(f"✗ FAIL - Status {response.status_code}")
            results['analisis_detalle'] = 'FAIL'
    else:
        print("⚠ SKIP - No hay resultados para probar detalle")
        results['analisis_detalle'] = 'SKIP'
except Exception as e:
    print(f"✗ ERROR - {e}")
    results['analisis_detalle'] = 'ERROR'

# ============================================================================
# TEST 3: /api/estadisticas/resumen/
# ============================================================================
print("\n\n[3] GET /api/estadisticas/resumen/")
print("-" * 80)
try:
    response = requests.get(f"{base_url}/api/estadisticas/resumen/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ PASS - Resumen obtenido")
        print(f"Total de noticias: {data.get('total_noticias')}")
        print(f"Total verificadas: {data.get('total_verificadas')}")
        print(f"Tipos de violencia: {data.get('tipos_violencia')}")
        print(f"Ámbitos: {data.get('ambitos')}")
        print(f"Top ciudades: {len(data.get('ciudades_top', []))} ciudades")
        results['estadisticas_resumen'] = 'PASS'
    else:
        print(f"✗ FAIL - Status {response.status_code}")
        results['estadisticas_resumen'] = 'FAIL'
except Exception as e:
    print(f"✗ ERROR - {e}")
    results['estadisticas_resumen'] = 'ERROR'

# ============================================================================
# TEST 4: /api/estadisticas/tendencia/
# ============================================================================
print("\n\n[4] GET /api/estadisticas/tendencia/")
print("-" * 80)
try:
    response = requests.get(f"{base_url}/api/estadisticas/tendencia/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ PASS - Tendencia obtenida")
        print(f"Períodos: {len(data)}")
        if data:
            print(f"Primer período:")
            print(json.dumps(data[0], indent=2, ensure_ascii=False))
        results['estadisticas_tendencia'] = 'PASS'
    else:
        print(f"✗ FAIL - Status {response.status_code}")
        results['estadisticas_tendencia'] = 'FAIL'
except Exception as e:
    print(f"✗ ERROR - {e}")
    results['estadisticas_tendencia'] = 'ERROR'

# ============================================================================
# TEST 5: /api/estadisticas/tipos/
# ============================================================================
print("\n\n[5] GET /api/estadisticas/tipos/")
print("-" * 80)
try:
    response = requests.get(f"{base_url}/api/estadisticas/tipos/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ PASS - Tipos de violencia obtenidos")
        print(f"Cantidad de tipos: {len(data)}")
        if data:
            print("Desglose:")
            for item in data:
                print(f"  - {item['tipo']}: {item['cantidad']} ({item['porcentaje']}%)")
        results['estadisticas_tipos'] = 'PASS'
    else:
        print(f"✗ FAIL - Status {response.status_code}")
        results['estadisticas_tipos'] = 'FAIL'
except Exception as e:
    print(f"✗ ERROR - {e}")
    results['estadisticas_tipos'] = 'ERROR'

print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)
for test, result in results.items():
    symbol = "✓" if result == 'PASS' else "✗"
    print(f"{symbol} {test:30} -> {result}")

all_pass = all(v == 'PASS' for v in results.values())
print("\n" + ("=" * 80))
if all_pass:
    print("✅ TODAS LAS PRUEBAS PASARON - FASE 1 100% COMPLETA")
else:
    print("⚠️  ALGUNAS PRUEBAS FALLARON")
print("=" * 80)
