from travelcompanion.config import OVERPASS_API_URL
from .api_utils import fetch_json

async def get_places(lat: float, lon: float, amenity: str | None, radius: int, limit: int) -> list[dict]:
    """
    Ищет места определённого типа поблизости с использованием Overpass API.

    :param lat: широта
    :param lon: долгота
    :param radius: радиус поиска в метрах
    :param amenity: тип места (например: restaurant, cafe, pharmacy и т.д.)
    :return: список словарей с информацией о найденных местах

    Пример элемента в исходном ответе Overpass API:
    {
        "type": "node",
        "id": 123456789,
        "lat": 55.7561,
        "lon": 37.6179,
        "tags": {
            "name": "Ресторан Иван",
            "amenity": "restaurant",
            "cuisine": "russian",
            "website": "http://ivan-restaurant.example"
        }
    }

    Пример элемента в возвращаемом списке:
    {
        "name": "Ресторан Иван",
        "lat": 55.7561,
        "lon": 37.6179,
        "address": "ул. Арбат, 12",
        "cuisine": "russian",
        "website": "http://ivan-restaurant.example",
        "phone": "+7 495 123-45-67"
    }
    """

    query = f"""
       [out:json];
       node(around:{radius},{lat},{lon})["amenity"="{amenity}"];
       out;
       """

    data = await fetch_json(url=OVERPASS_API_URL, params={"data": query})

    result = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        result.append(
            {
                "name": tags.get("name", "Без названия"),
                "lat": el.get("lat"),
                "lon": el.get("lon"),
                "address": tags.get("addr:street", "") + tags.get("addr:housenumber", ""),
                "category": tags.get("amenity")
            }
        )

    return result

