import requests
import json
import time

# Esperar a que el servidor esté listo
print("Esperando servidor...")
time.sleep(2)

print("=" * 70)
print("VALIDACIÓN FASE 1 - ANÁLISIS + ESTADÍSTICAS")
print("=" * 70)

# Test de rutas
endpoints = [
    ("GET", "http://localhost:8000/api/analisis/resultados/", "Lista de resultados"),
    ("GET", "http://localhost:8000/api/estadisticas/resumen/", "Resumen de estadísticas"),
    ("GET", "http://localhost:8000/api/estadisticas/tendencia/", "Tendencia mensual"),
    ("GET", "http://localhost:8000/api/estadisticas/tipos/", "Conteo de tipos"),
]

results = []
for method, url, descripcion in endpoints:
    try:
        print(f"\n[TEST] {descripcion}")
        print(f"  URL: {url}")
        
        response = requests.get(url)
        status_code = response.status_code
        
        print(f"  Status: {status_code}", end="")
        
        if status_code == 200:
            print(" ✓")
            data = response.json()
            
            # Mostrar estructura
            if isinstance(data, list):
                print(f"  Array con {len(data)} items")
                if data:
                    print(f"  Primer item: {json.dumps(data[0], indent=4, ensure_ascii=False)[:200]}...")
            elif isinstance(data, dict):
                print(f"  Objeto con keys: {list(data.keys())}")
                print(f"  Contenido: {json.dumps(data, indent=4, ensure_ascii=False)[:300]}...")
            
            results.append((descripcion, "✓ PASS"))
        else:
            print(" ✗")
            print(f"  Error: {response.text[:200]}")
            results.append((descripcion, "✗ FAIL"))
            
    except Exception as e:
        print(f" ✗")
        print(f"  Excepción: {e}")
        results.append((descripcion, f"✗ ERROR: {e}"))

print("\n" + "=" * 70)
print("RESUMEN DE RESULTADOS")
print("=" * 70)
for descripcion, resultado in results:
    print(f"{resultado:12} | {descripcion}")

print("\n" + "=" * 70)
all_passed = all("✓" in r for _, r in results)
if all_passed:
    print("✅ TODAS LAS PRUEBAS PASARON")
else:
    print("❌ ALGUNAS PRUEBAS FALLARON")
print("=" * 70)
