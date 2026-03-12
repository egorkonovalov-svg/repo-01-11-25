from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from models.user import User
from crypt_module import create_password_hash, create_jwt_token, is_password_correct
from database import async_session_maker


class RegisterRequest(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


async def register_user(data: RegisterRequest) -> str:
    password_hash = await create_password_hash(password=data.password)
    async with async_session_maker() as session:
        new_user = User(
            UserName=data.username,
            Email=data.email,
            PasswordHash=password_hash,
            Name=data.name,
        )
        session.add(new_user)
        await session.commit()
    return await create_jwt_token(email=data.email)


async def login_check(data: LoginRequest) -> str | None:
    """Validate credentials and return a JWT token, or None on failure."""
    password_hash = await _get_password_hash(email=data.email)
    if password_hash is None:
        return None

    if not await is_password_correct(data.password, password_hash):
        return None

    return await create_jwt_token(email=data.email)


async def _get_password_hash(email: str) -> bytes | None:
    async with async_session_maker() as session:
        query = select(User).where(User.Email == email)
        result = await session.execute(query)
        user = result.scalars().first()
        return user.PasswordHash if user else None


async def get_user_info(email: str) -> User | None:
    async with async_session_maker() as session:
        query = select(User).where(User.Email == email)
        result = await session.execute(query)
        return result.scalars().first()


async def get_user_by_id(user_id: int) -> User | None:
    async with async_session_maker() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()
