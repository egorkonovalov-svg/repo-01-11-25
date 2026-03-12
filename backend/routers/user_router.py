from fastapi import HTTPException, APIRouter, Depends, Response

from dependencies import get_current_user_id
from services.user_service import (
    RegisterRequest,
    LoginRequest,
    register_user,
    login_check,
    get_user_by_id,
)

user_router = APIRouter(prefix='/api/v1/auth')

COOKIE_MAX_AGE = 7 * 24 * 60 * 60  # 7 days


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
    )


@user_router.post("/register")
async def register(data: RegisterRequest, response: Response):
    jwt_token = await register_user(data)
    if not jwt_token:
        raise HTTPException(status_code=400, detail="Registration failed")

    _set_auth_cookie(response, jwt_token)
    return {"message": "Registration successful", "token": jwt_token}


@user_router.post("/login")
async def login(data: LoginRequest, response: Response):
    jwt_token = await login_check(data)
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    _set_auth_cookie(response, jwt_token)
    return {"message": "Login successful", "token": jwt_token}


@user_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token", httponly=True, secure=True, samesite="lax"
    )
    return {"message": "Logout successful"}


@user_router.get("/me")
async def get_current_user(user_id: int = Depends(get_current_user_id)):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.Email,
        "name": user.Name,
        "username": user.UserName,
    }
