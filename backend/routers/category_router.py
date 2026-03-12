from typing import Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException

from models.transaction import TransactionType
from dependencies import get_current_user_id
from services.category_service import (
    create_category,
    get_category_by_id,
    get_user_categories,
    update_category,
    delete_category,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

category_router = APIRouter(prefix='/api/v1/category')


@category_router.post("/", response_model=CategoryResponse)
async def create_category_endpoint(
    data: CategoryCreate,
    user_id: int = Depends(get_current_user_id),
):
    return await create_category(user_id, data)


@category_router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    type: Optional[TransactionType] = Query(None, description="Фильтр по типу транзакции"),
    user_id: int = Depends(get_current_user_id),
):
    return await get_user_categories(user_id, type)


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    user_id: int = Depends(get_current_user_id),
):
    category = await get_category_by_id(category_id, user_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(
    category_id: int,
    data: CategoryUpdate,
    user_id: int = Depends(get_current_user_id),
):
    return await update_category(category_id, user_id, data)


@category_router.delete("/{category_id}")
async def delete_category_endpoint(
    category_id: int,
    user_id: int = Depends(get_current_user_id),
):
    await delete_category(category_id, user_id)
    return {"message": "Category deleted successfully"}
