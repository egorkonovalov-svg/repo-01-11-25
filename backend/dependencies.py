from fastapi import HTTPException, Cookie

from crypt_module import verify_jwt_token
from services.user_service import get_user_info


async def _resolve_user_id(access_token: str | None) -> int:
    """Extract and validate user_id from a JWT access token."""
    if not access_token:
        raise HTTPException(status_code=401, detail="Authentication cookie missing")

    payload = await verify_jwt_token(access_token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_info(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user.id


async def get_current_user_id(access_token: str = Cookie(None)) -> int:
    """FastAPI dependency: get user_id from JWT cookie."""
    return await _resolve_user_id(access_token)


async def get_user_id_from_cookie(access_token: str | None) -> int:
    """Standalone helper: get user_id from a raw token string (no Depends)."""
    return await _resolve_user_id(access_token)
