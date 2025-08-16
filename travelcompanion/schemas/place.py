from pydantic import BaseModel

class PlaceBase(BaseModel):
    category_id: int
    name: str
    rating: float | None = None
    price_range: str | None = None
    latitude: float
    longitude: float
    address: str | None
    api_source: str | None = None

class PlaceCreate(PlaceBase):
    pass

class PlaceRead(PlaceBase):
    pass