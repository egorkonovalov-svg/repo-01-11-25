from typing import Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException

from dependencies import get_current_user_id
from services.budget_service import (
    create_budget,
    get_budget_by_id,
    get_user_budgets,
    update_budget,
    delete_budget,
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse,
)

budget_router = APIRouter(prefix='/api/v1/budget')


@budget_router.post("/", response_model=BudgetResponse)
async def create_budget_endpoint(
    data: BudgetCreate,
    user_id: int = Depends(get_current_user_id),
):
    return await create_budget(user_id, data)


@budget_router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    user_id: int = Depends(get_current_user_id),
):
    return await get_user_budgets(user_id, is_active, category_id)


@budget_router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    user_id: int = Depends(get_current_user_id),
):
    budget = await get_budget_by_id(budget_id, user_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@budget_router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget_endpoint(
    budget_id: int,
    data: BudgetUpdate,
    user_id: int = Depends(get_current_user_id),
):
    return await update_budget(budget_id, user_id, data)


@budget_router.delete("/{budget_id}")
async def delete_budget_endpoint(
    budget_id: int,
    user_id: int = Depends(get_current_user_id),
):
    await delete_budget(budget_id, user_id)
    return {"message": "Budget deleted successfully"}
