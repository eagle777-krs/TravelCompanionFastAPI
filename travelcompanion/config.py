import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_ECHO = True

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
GEOAPIFY_PLACES_API_URL = "https://api.geoapify.com/v2/places"
FOURSQUARE_URL = "https://api.foursquare.com/v3/places/search"

FOURSQUARE_API_KEY = ""
GEOAPIFY_PLACES_API_KEY = os.getenv("GEOAPIFY_API")