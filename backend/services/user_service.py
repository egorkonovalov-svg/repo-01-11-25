from models.user import *
from crypt_module import create_password_hash, create_jwt_token, is_password_correct
from database import async_session_maker
from sqlalchemy import select
from pydantic import BaseModel

# Запрос регистрации
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


async def register_user(data: RegisterRequest) -> str:
    """
    INSERT INTO users ($email, $passwordhash, $name)
    """
    passwordhash = await create_password_hash(password=data.password)
    async with async_session_maker() as session:
        new_user = User(
            Email=data.email,
            PasswordHash=passwordhash,
            Name=data.name
        )
        session.add(new_user)
        await session.commit()
    jwt_token = await create_jwt_token(email=data.email)
    return jwt_token


async def get_password_hash(email: str) -> bytes:
    """
    SELECT passwordhash FROM users WHERE Email == $email
    """
    async with async_session_maker() as session:
        query_select = select(User).where(User.Email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data.PasswordHash


async def login_check(data: LoginRequest) -> str:
    passwordhash = await get_password_hash(email=data.email)
    if not passwordhash:
        return 'error'
    success = await is_password_correct(data.password, passwordhash)
    if success:
        jwttoken = await create_jwt_token(email=data.email)
        return jwttoken
    else:
        return 'error'

async def get_user_info(email: str) -> User:
    """
    SELECT * FROM users WHERE Email = $email
    """
    async with async_session_maker() as session:
        query_select = select(User).where(User.Email == email)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data


async def get_user_by_id(user_id: int) -> User:
    """
    SELECT * FROM users WHERE id = $user_id
    """
    async with async_session_maker() as session:
        query_select = select(User).where(User.id == user_id)
        result = await session.execute(query_select)
        user_data = result.scalars().first()
        return user_data

