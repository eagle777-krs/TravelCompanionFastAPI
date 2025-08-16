from travelcompanion.config import OVERPASS_URL
from .api_utils import fetch_json

async def get_places(lat: float, lon: float, radius:int = 3000, amenity: str = "restaurant") -> list[dict]:
    '''
    :param lat: широта
    :param lon: долгота
    :param radius: радиус поиска в метрах
    :param amenity: тип места (restaurant, cafe, pharmacy и т.д.)
    :return (пример ответа):
    {
  "version": 0.6,
  "generator": "Overpass API 0.7.56.7 3079d8ea",
  "osm3s": {
    "timestamp_osm_base": "2025-08-16T10:30:02Z",
    "copyright": "The data included..."
  },
  "elements": [
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
    '''
    query = f"""
       [out:json];
       node(around:{radius},{lat},{lon})["amenity"="{amenity}"];
       out;
       """

    data = await fetch_json(url=OVERPASS_URL, params={"data": query})

    result = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        result.append(
            {
                "name": tags.get("name", "Без названия"),
                "lat": el.get("lat"),
                "lon": el.get("lon"),
                "amenity": tags.get("amenity")
            }
        )

    return result

