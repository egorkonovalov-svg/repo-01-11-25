import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from services.category_service import (
    create_category,
    get_category_by_id,
    get_user_categories,
    update_category,
    delete_category,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)
from models.transaction import TransactionType
from dependencies import get_current_user_id

category_router = APIRouter(prefix='/category')


@category_router.post("/", response_model=CategoryResponse)
async def create_category_endpoint(
    data: CategoryCreate,
    user_id: int = Depends(get_current_user_id)
):
    """Создать новую категорию"""
    return await create_category(user_id, data)


@category_router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    type: Optional[TransactionType] = Query(None, description="Фильтр по типу транзакции"),
    user_id: int = Depends(get_current_user_id)
):
    """Получить все категории пользователя"""
    return await get_user_categories(user_id, type)


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Получить категорию по ID"""
    category = await get_category_by_id(category_id, user_id)
    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(
    category_id: int,
    data: CategoryUpdate,
    user_id: int = Depends(get_current_user_id)
):
    """Обновить категорию"""
    return await update_category(category_id, user_id, data)


@category_router.delete("/{category_id}")
async def delete_category_endpoint(
    category_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Удалить категорию"""
    await delete_category(category_id, user_id)
    return {"message": "Category deleted successfully"}
