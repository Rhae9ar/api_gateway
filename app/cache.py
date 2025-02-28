from redis import Redis
import json

class Cache:
    def __init__(self, redis_client: Redis, expiration: int = 60):
        self.redis_client = redis_client
        self.expiration = expiration

    def get(self, key: str):
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value, expiration: int = None):
        if expiration is None:
            expiration = self.expiration
        self.redis_client.set(key, json.dumps(value), ex=expiration)

    def delete(self, key: str):
        self.redis_client.delete(key)