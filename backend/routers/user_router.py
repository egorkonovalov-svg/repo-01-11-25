import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from services.user_service import *
from dependencies import get_current_user_id
from fastapi import HTTPException, APIRouter, Depends, Response

user_router = APIRouter(prefix='/auth')

@user_router.post("/register")
async def register(data: RegisterRequest, response: Response):
    jwt_token = await register_user(data)
    if jwt_token and jwt_token != 'error':
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 дней
        )
        return {"message": "Registration successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=400, detail="Registration failed")


@user_router.post("/login")
async def login(data: LoginRequest, response: Response):
    jwt_token = await login_check(data)
    if jwt_token and jwt_token != 'error':
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 дней
        )
        return {"message": "Login successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")


@user_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True, secure=True, samesite="lax")
    return {"message": "Logout successful"}


@user_router.get("/me")
async def get_current_user(user_id: int = Depends(get_current_user_id)):
    """Получить информацию о текущем пользователе"""
    from services.user_service import get_user_by_id
    
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.Email,
        "name": user.Name,
        "username": user.UserName
    }
