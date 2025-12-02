import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import Depends, HTTPException, Header
from crypt_module import verify_jwt_token
from services.user_service import get_user_info


async def get_current_user_id(authorization: str = Header(None)) -> int:
    """Получить user_id из JWT токена"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Формат: "Bearer <token>"
        token = authorization.replace("Bearer ", "").strip()
        payload = await verify_jwt_token(token)
        email = payload.get("sub")
        
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await get_user_info(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

