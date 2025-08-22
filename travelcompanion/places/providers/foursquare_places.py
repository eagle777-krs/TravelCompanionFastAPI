from travelcompanion.config import FOURSQUARE_API_KEY, FOURSQUARE_URL
from .api_utils import fetch_json

async def get_places(lat: float, lon: float, amenity: str | None, radius: int, limit: int) -> list[dict]:
    """
    Получает места рядом через Foursquare API.

    :param lat: широта
    :param lon: долгота
    :param radius: радиус поиска (м)
    :param amenity: строка поиска ("restaurant", "cafe", "pharmacy" и т.д.)
    :return: список объектов с name, lat, lon, categories
    """
    headers = {
        "Authorization": FOURSQUARE_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "ll": f"{lat},{lon}",
        "radius": radius,
        "query": amenity,
        "limit": {limit}
    }

    data = await fetch_json(url=FOURSQUARE_URL, params=params | {"headers": headers})

    result = []
    for el in data.get("results", []):
        coords = el.get("geocodes", {}).get("main", {})
        categories = [c["name"] for c in el.get("categories", [])]
        result.append({
            "id": el.get("fsq_id"),
            "name": el.get("name", "Без названия"),
            "lat": coords.get("latitude"),
            "lon": coords.get("longitude"),
            "address": el.get("location", {}).get("address")
        })

    return result