from models.category import Category
from models.transaction import TransactionType
from database import async_session_maker
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, List
from fastapi import HTTPException


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: TransactionType
    is_default: bool = False


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[TransactionType] = None
    is_default: Optional[bool] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: TransactionType
    is_default: bool
    user_id: int

    class Config:
        from_attributes = True


async def create_category(user_id: int, data: CategoryCreate) -> Category:
    """Создать новую категорию"""
    async with async_session_maker() as session:
        new_category = Category(
            name=data.name,
            description=data.description,
            type=data.type,
            is_default=data.is_default,
            user_id=user_id
        )
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category


async def get_category_by_id(category_id: int, user_id: int) -> Optional[Category]:
    """Получить категорию по ID"""
    async with async_session_maker() as session:
        query = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
        result = await session.execute(query)
        return result.scalars().first()


async def get_user_categories(user_id: int, type: Optional[TransactionType] = None) -> List[Category]:
    """Получить все категории пользователя"""
    async with async_session_maker() as session:
        query = select(Category).where(Category.user_id == user_id)
        if type:
            query = query.where(Category.type == type)
        result = await session.execute(query)
        return list(result.scalars().all())


async def update_category(category_id: int, user_id: int, data: CategoryUpdate) -> Category:
    """Обновить категорию"""
    async with async_session_maker() as session:
        query = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
        result = await session.execute(query)
        category = result.scalars().first()
        
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        if data.name is not None:
            category.name = data.name
        if data.description is not None:
            category.description = data.description
        if data.type is not None:
            category.type = data.type
        if data.is_default is not None:
            category.is_default = data.is_default
        
        await session.commit()
        await session.refresh(category)
        return category


async def delete_category(category_id: int, user_id: int) -> bool:
    """Удалить категорию"""
    async with async_session_maker() as session:
        query = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id
        )
        result = await session.execute(query)
        category = result.scalars().first()
        
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        await session.delete(category)
        await session.commit()
        return True

