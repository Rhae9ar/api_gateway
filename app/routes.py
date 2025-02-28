from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from prometheus_client import generate_latest

import app
from .auth import authenticate_user, create_access_token, Token, User, get_current_user

from datetime import timedelta

from .rate_limiter import RateLimiter
from .config import redis_client
from .cache import Cache

from .main import REQUESTS, REQUEST_TIMES, REGISTRY

import time


router = APIRouter()
rate_limiter = RateLimiter(redis_client, limit=10, period=60)
cache = Cache(redis_client, expiration=60)

@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if not rate_limiter.is_allowed(request.client.host):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    user = authenticate_user(User(username=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/items/{item_id}")
async def read_item(item_id: int, request: Request):
    start_time = time.time()
    REQUESTS.inc()
    cached_item = cache.get(f"item:{item_id}")
    if cached_item:
        return cached_item

    item = {"item_id": item_id, "name": f"Item {item_id}"}

    cache.set(f"item:{item_id}", item)

    REQUEST_TIMES.observe(time.time() - start_time)
    return item

@router.get("/users/me")
async def read_user_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain")