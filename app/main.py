from fastapi import FastAPI

from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer

from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

from .auth import decode_access_token
from .routes import router

REQUESTS = Counter('requests_total', 'Total number of requests')
REQUEST_TIMES = Histogram('request_latency_seconds', 'Request latency in seconds')


app = FastAPI()

app.include_router(router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/ping")
async def ping():
    return {"message": "pong"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return username

@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}!"}