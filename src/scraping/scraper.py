"""
Recolector de datos de estacionamientos en Santiago.
Fuentes: Google Maps Places API + scraping de sitios públicos.
"""
import requests
import time
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
BASE_URL = "https://maps.googleapis.com/maps/api/place"

COMUNAS_COORDS = {
    'Las Condes':      (-33.4133, -70.5836),
    'Providencia':     (-33.4326, -70.6093),
    'Santiago Centro': (-33.4500, -70.6667),
    'Ñuñoa':           (-33.4569, -70.5989),
    'Vitacura':        (-33.3950, -70.5789),
    'Maipú':           (-33.5078, -70.7581),
    'La Florida':      (-33.5246, -70.5983),
}


def buscar_estacionamientos_google(lat: float, lng: float, radio: int = 1500) -> list:
    """Busca estacionamientos via Google Places API Nearby Search."""
    if not GOOGLE_API_KEY:
        print("  Sin GOOGLE_MAPS_API_KEY — saltando búsqueda real")
        return []

    url = f"{BASE_URL}/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radio,
        "type": "parking",
        "key": GOOGLE_API_KEY,
        "language": "es",
    }
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    return data.get("results", [])


def parsear_lugar(lugar: dict, comuna: str) -> dict:
    """Extrae campos relevantes de un resultado de Google Places."""
    return {
        "nombre":    lugar.get("name", ""),
        "direccion": lugar.get("vicinity", ""),
        "comuna":    comuna,
        "lat":       lugar["geometry"]["location"]["lat"],
        "lng":       lugar["geometry"]["location"]["lng"],
        "rating":    lugar.get("rating", None),
        "reviews":   lugar.get("user_ratings_total", 0),
        "place_id":  lugar.get("place_id", ""),
        "fuente":    "google_maps",
    }


def recolectar_todas_las_comunas() -> pd.DataFrame:
    """Itera por todas las comunas y recolecta estacionamientos."""
    registros = []
    for comuna, (lat, lng) in COMUNAS_COORDS.items():
        print(f"Buscando en {comuna}...")
        lugares = buscar_estacionamientos_google(lat, lng)
        for lugar in lugares:
            registros.append(parsear_lugar(lugar, comuna))
        time.sleep(0.5)  # Respetar rate limits

    df = pd.DataFrame(registros)
    print(f"\nTotal recolectado: {len(df)} estacionamientos")
    return df


if __name__ == '__main__':
    df = recolectar_todas_las_comunas()
    if not df.empty:
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/estacionamientos_raw.csv', index=False, encoding='utf-8-sig')
        print("Guardado en data/raw/estacionamientos_raw.csv")
    else:
        print("Sin datos reales. Ejecuta generar_datos_ejemplo.py para continuar.")
