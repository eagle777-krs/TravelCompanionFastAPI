from .api_utils import fetch_json
from travelcompanion.config import GEOGRAPHY_PLACES_API_URL, GEOGRAPHY_PLACES_API_KEY

async def get_places(lat: float, lon: float, radius: int = 1000, amenity: str = "catering.restaurant", limit=10) -> list[dict]:

    """
       Ищет места поблизости с использованием Geoapify Places API.

       :param lat: широта (например, 55.7558 для Москвы)
       :param lon: долгота (например, 37.6176 для Москвы)
       :param radius: радиус поиска в метрах (по умолчанию 1000)
       :param amenity: категория мест (например: "catering.restaurant", "catering.cafe", "shop.supermarket")
                       Можно передавать несколько категорий через запятую.
       :param limit: максимальное количество результатов (по умолчанию 10)
       :return: список словарей с информацией о найденных местах

       Пример элемента в исходном ответе Geoapify API (усечённый):
       {
           "type": "Feature",
           "geometry": {
               "type": "Point",
               "coordinates": [37.6176, 55.7558]
           },
           "properties": {
               "name": "Ресторан Иван",
               "categories": ["catering.restaurant"],
               "address_line1": "ул. Арбат, 12",
               "city": "Москва",
               "postcode": "119002",
               "country": "Россия",
               "rating": 4.2
           }
       }

       Пример элемента в возвращаемом списке:
       {
           "name": "Ресторан Иван",
           "lon": 37.6176,
           "lat": 55.7558,
           "rating": 4.2,
           "address": "ул. Арбат, 12"
       }
       """

    params = {
        "categories": amenity,
        "filter": f"circle:{lon},{lat},{radius}",
        "limit": limit,
        "apiKey": GEOGRAPHY_PLACES_API_KEY
    }

    data = await fetch_json(url=GEOGRAPHY_PLACES_API_URL, params=params)

    result = []
    for el in data.get("features", []):
        prop = el.get("properties", {})
        result.append(
            {
                "name": prop.get("name", "Без названия"),
                "lon": el.get("geometry", {}).get("coordinates", [None, None])[0],
                "lat": el.get("geometry", {}).get("coordinates", [None, None])[1],
                "rating": prop.get("rating", None),
                "address": prop.get("address_line1", None)
            }
        )
    return result