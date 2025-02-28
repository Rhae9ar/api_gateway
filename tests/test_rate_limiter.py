from app.rate_limiter import RateLimiter
from redis import Redis
import time

def test_rate_limiter():
    redis_client = Redis(host="localhost", port=6379, db=0)
    rate_limiter = RateLimiter(redis_client, limit=2, period=1)
    key = "test_key"

    assert rate_limiter.is_allowed(key)
    assert rate_limiter.is_allowed(key)
    assert not rate_limiter.is_allowed(key)

    time.sleep(1)
    assert rate_limiter.is_allowed(key)