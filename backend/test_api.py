import requests
import json
import time

# Esperar a que el servidor esté listo
time.sleep(2)

print("=" * 60)
print("PRUEBA DE ENDPOINTS API")
print("=" * 60)

try:
    # Test GET /api/resultados/
    print("\n[1] GET /api/resultados/")
    response = requests.get('http://localhost:8000/api/resultados/')
    print(f"    Status: {response.status_code}")
    print(f"    Response: {json.dumps(response.json(), indent=2)}")
    
    # Test GET /api/resultados/{nombre}/
    if response.status_code == 200 and response.json():
        primer_resultado = response.json()[0]
        nombre = primer_resultado['nombre']
        print(f"\n[2] GET /api/resultados/{nombre}/")
        response = requests.get(f'http://localhost:8000/api/resultados/{nombre}/')
        print(f"    Status: {response.status_code}")
        print(f"    Response: {json.dumps(response.json(), indent=2)}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
