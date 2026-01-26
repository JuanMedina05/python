import requests

API_URL = "http://api.anhqv-stats.es/api/characters"

def obtener_characters():
    print("Llamando a API:", API_URL)
    response = requests.get(API_URL, verify=False)
    print("Status code:", response.status_code)
    print("Texto de respuesta:", response.text[:200])  # primeras 200 chars
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])
