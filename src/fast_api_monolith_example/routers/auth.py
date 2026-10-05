from fastapi import APIRouter

from .auth.models import LoginRequest, RegisterRequest
from aut.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/auth/register")
def register(request: RegisterRequest):
    return {"message": "User registered successfully"}

@router.post("/auth/login")
def login(request: LoginRequest):
    return {"message": "User logged in successfully"}