from app.backend.services.user_service import *
from app.backend.crypt_module import *
from fastapi import HTTPException, APIRouter, Header



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
