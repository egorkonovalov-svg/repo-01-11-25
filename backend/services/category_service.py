from typing import Optional, List

from sqlalchemy import select
from pydantic import BaseModel
from fastapi import HTTPException

from models.category import Category
from models.transaction import TransactionType
from database import async_session_maker


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
    async with async_session_maker() as session:
        new_category = Category(
            name=data.name,
            description=data.description,
            type=data.type,
            is_default=data.is_default,
            user_id=user_id,
        )
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category


async def get_category_by_id(category_id: int, user_id: int) -> Optional[Category]:
    async with async_session_maker() as session:
        query = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )
        result = await session.execute(query)
        return result.scalars().first()


async def get_user_categories(user_id: int, type: Optional[TransactionType] = None) -> List[Category]:
    async with async_session_maker() as session:
        query = select(Category).where(Category.user_id == user_id)
        if type:
            query = query.where(Category.type == type)
        result = await session.execute(query)
        return list(result.scalars().all())


async def update_category(category_id: int, user_id: int, data: CategoryUpdate) -> Category:
    async with async_session_maker() as session:
        query = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )
        result = await session.execute(query)
        category = result.scalars().first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        update_fields = data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(category, field, value)

        await session.commit()
        await session.refresh(category)
        return category


async def delete_category(category_id: int, user_id: int) -> bool:
    async with async_session_maker() as session:
        query = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )
        result = await session.execute(query)
        category = result.scalars().first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        await session.delete(category)
        await session.commit()
        return True
