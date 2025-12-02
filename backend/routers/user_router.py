import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from ..services.user_service import *
from fastapi import HTTPException, APIRouter

user_router = APIRouter(prefix='/auth')

@user_router.post("/register")
async def register(data: RegisterRequest):
    jwt_token = await register_user(data)
    return {"message": "Registration successful", "token": jwt_token}


@user_router.post("/login")
async def login(data: LoginRequest):
    jwt_token = await login_check(data)
    if jwt_token:
        return {"message": "Registration successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
