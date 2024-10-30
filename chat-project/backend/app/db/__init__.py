from app.db.hashmap_db import HashmapDB
from app.db.redis_db import RedisDB
from app.repository.database import Database


def create_default_db()->Database:
    # return RedisDB()
    return HashmapDB('.')