from pydantic import BaseModel

class PlaceBase(BaseModel):
    name: str
    rating: float | None = None
    price_range: str | None = None
    latitude: float
    longitude: float
    address: str | None
    api_source: str | None = None
    place_code: str

class PlaceCreate(PlaceBase):
    category_name: str
    pass

class PlaceRead(PlaceBase):
    pass