from fastapi import APIRouter, HTTPException, Request, Response, Form
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from starlette.responses import RedirectResponse

router = APIRouter()

# Simulated user database (replace with real DB later)
USER_DB = {
    "admin": {"password": "admin123", "role": "admin"},
    "john": {"password": "johnpass", "role": "admin"},
    "marc": {"password": "marcpass", "role": "viewer"},
    "guest": {"password": "guestpass", "role": "viewer"},
}

def login_check(username, password):
    user = USER_DB.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None