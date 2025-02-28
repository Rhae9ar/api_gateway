from redis import Redis
from time import time

class RateLimiter:
    def __init__(self, redis_client: Redis, limit: int, period: int):
        self.redis_client = redis_client
        self.limit = limit
        self.period = period

    def is_allowed(self, key: str) -> bool:
        now = int(time())
        with self.redis_client.pipeline() as pipe:
            pipe.zremrangebyscore(key, 0, now - self.period)
            pipe.zcard(key)
            pipe.zadd(key, {now: now})
            count, _ = pipe.execute()
        return count < self.limit