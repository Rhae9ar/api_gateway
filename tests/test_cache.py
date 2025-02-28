from app.cache import Cache
from redis import Redis
import time

def test_cache():
    redis_client = Redis(host="localhost", port=6379, db=0)
    cache = Cache(redis_client, expiration=1)
    key = "test_key"
    value = {"test": "value"}

    assert cache.get(key) is None
    cache.set(key, value)
    assert cache.get(key) == value
    time.sleep(1)
    assert cache.get(key) is None