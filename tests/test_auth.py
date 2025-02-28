from app.auth import create_access_token, authenticate_user, User

import jwt
from datetime import timedelta

SECRET_KEY = "test_secret_key"
ALGORITHM = "HS256"

def test_create_access_token():
    token = create_access_token(data={"sub": "testuser"}, secret_key=SECRET_KEY, algorithm=ALGORITHM)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == "testuser"

def test_authenticate_user():
    user = User(username="testuser", password="password")
    authenticated_user = authenticate_user(user, "testuser", "password")
    assert authenticated_user == user

def test_authenticate_user_invalid_password():
    user = User(username="testuser", password="password")
    authenticated_user = authenticate_user(user, "testuser", "wrongpassword")
    assert authenticated_user is None