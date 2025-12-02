import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from services.budget_service import (
    create_budget,
    get_budget_by_id,
    get_user_budgets,
    update_budget,
    delete_budget,
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse
)
from dependencies import get_current_user_id

budget_router = APIRouter(prefix='/budget')


@budget_router.post("/", response_model=BudgetResponse)
async def create_budget_endpoint(
    data: BudgetCreate,
    user_id: int = Depends(get_current_user_id)
):
    """Создать новый бюджет"""
    return await create_budget(user_id, data)


@budget_router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    user_id: int = Depends(get_current_user_id)
):
    """Получить все бюджеты пользователя"""
    return await get_user_budgets(user_id, is_active, category_id)


@budget_router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Получить бюджет по ID"""
    budget = await get_budget_by_id(budget_id, user_id)
    if not budget:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@budget_router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget_endpoint(
    budget_id: int,
    data: BudgetUpdate,
    user_id: int = Depends(get_current_user_id)
):
    """Обновить бюджет"""
    return await update_budget(budget_id, user_id, data)


@budget_router.delete("/{budget_id}")
async def delete_budget_endpoint(
    budget_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Удалить бюджет"""
    await delete_budget(budget_id, user_id)
    return {"message": "Budget deleted successfully"}
