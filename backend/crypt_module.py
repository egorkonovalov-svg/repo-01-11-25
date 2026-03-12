import time

import bcrypt
import jwt
from fastapi import HTTPException

from services.config import SECRET_TOKEN

TOKEN_EXPIRY_SECONDS = 7 * 24 * 60 * 60  # 7 days


async def verify_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_TOKEN, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def create_jwt_token(email: str) -> str:
    payload = {
        "sub": email,
        "iss": "Finance_monitor",
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_EXPIRY_SECONDS,
    }
    return jwt.encode(payload, SECRET_TOKEN, algorithm="HS256")


async def create_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def is_password_correct(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)
