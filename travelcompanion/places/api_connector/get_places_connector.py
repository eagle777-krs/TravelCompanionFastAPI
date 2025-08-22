import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from travelcompanion.models.models import Place, Category
from travelcompanion.places.providers import foursquare_places, geoapify_places, open_street_map
from travelcompanion.schemas.place import PlaceCreate

async def is_place_exist_in_db(session: AsyncSession, place: PlaceCreate) -> bool:
    '''
    Смотрим, есть ли это место в БД
    :param session:
    :param place:
    :return:
    '''
    db_query_result = await session.execute(select(Place.id).where(Place.place_code == place.place_code))

    return db_query_result.scalar_one_or_none() is not None

async def fetch_all_places(lat: float, lon: float, amenity: str | None = None, radius: int = 3000, limit: int =10) -> list[PlaceCreate]:
    """
    Соединяет инфу с трёх прсеров в один лист, избегает дубликатов, но при этом равномерно подтягивает информацию с
    трёх парсеров, предотвращая появление None в значениях полей. Если изначальная категория None, то передаётся
    категория из результата запроса.
    :param lat:
    :param lon:
    :param amenity:
    :param radius:
    :param limit:
    :return:
    """
    results = await asyncio.gather(
        foursquare_places.get_places(lat, lon, amenity, radius, limit),
        geoapify_places.get_places(lat, lon, amenity, radius, limit),
        open_street_map.get_places(lat, lon, amenity, radius, limit)
    )

    unified = {}
    for source, places in zip(["foursquare", "overpass", "osm"], results):
        for p in places:
            category = amenity or p.get("category")
            place_code = (p.get("name") or "") + str(p.get("lat")) + str(p.get("lon"))

            if place_code not in unified:
                unified[place_code] = PlaceCreate(
                    name=p.get("name"),
                    rating=p.get("rating"),
                    price_range=p.get("price_range"),
                    latitude=p.get("lat"),
                    longitude=p.get("lon"),
                    address=p.get("address"),
                    api_source=source,
                    place_code=place_code,
                    category_name=category
                )
            else:
                existing = unified[place_code]
                for field in ["rating", "price_range", "address", "category_name"]:
                    if getattr(existing, field) is None and p.get(field) is not None:
                        setattr(existing, field, p.get(field))
    return list(unified.values())

async def save_places(session: AsyncSession, places: list[PlaceCreate]):
    category_map = {}

    categories = {p.category_name for p in places if p.category_name}
    for c in categories:
        category = await session.execute(select(Category).where(Category.name == c))
        categ = category.scalar_one_or_none()
        if categ:
            category_map[categ.name] = categ.id

    for cname in categories:
        if cname not in category_map:
            category = Category(name=cname)
            session.add(category)
            await session.flush()
            category_map[cname] = category.id

    for p in places:
        new_place = Place(
            category_id=category_map.get(p.category_name, None),
            name=p.name,
            rating=p.rating,
            price_range=p.price_range,
            latitude=p.latitude,
            longitude=p.longitude,
            address=p.address,
            api_source=p.api_source,
            place_code=p.place_code
        )
        session.add(new_place)

    await session.commit()
