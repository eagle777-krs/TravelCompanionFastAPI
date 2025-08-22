from .api_utils import fetch_json
from travelcompanion.config import GEOAPIFY_PLACES_API_KEY, GEOAPIFY_PLACES_API_URL

async def get_places(lat: float, lon: float, amenity: str | None, radius: int, limit: int) -> list[dict]:

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
        "apiKey": GEOAPIFY_PLACES_API_KEY
    }

    data = await fetch_json(url=GEOAPIFY_PLACES_API_URL, params=params)

    result = []
    for el in data.get("features", []):
        prop = el.get("properties", {})
        categories = prop.get("categories")
        cat_val = None if len(categories) == 0 else categories[0]
        result.append(
            {
                "name": prop.get("name", "Без названия"),
                "lon": el.get("geometry", {}).get("coordinates", None)[0],
                "lat": el.get("geometry", {}).get("coordinates", None)[1],
                "rating": prop.get("rating", None),
                "address": prop.get("address_line1", None),
                "category": cat_val
            }
        )
    return result