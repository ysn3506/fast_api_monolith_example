from fastapi import APIRouter

from .models.auth import UserLogin, UserRegister


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/auth/register")
def register(request: UserRegister):
    return {"message": "User registered successfully"}

@router.post("/auth/login")
def login(request: UserLogin):
    return {"message": "User logged in successfully"}