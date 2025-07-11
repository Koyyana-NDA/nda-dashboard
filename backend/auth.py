from fastapi import APIRouter, HTTPException, Request, Response, Form
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from starlette.responses import RedirectResponse

router = APIRouter()

# Simulated user database (replace with real DB later)
users_db = {
    "koyyana": {"password": bcrypt.hash("adminpass"), "role": "admin"},
    "john": {"password": bcrypt.hash("john123"), "role": "director"},
    "guest": {"password": bcrypt.hash("guest"), "role": "viewer"}
}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_db.get(username)
    if not user or not bcrypt.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "username": username, "role": user["role"]}