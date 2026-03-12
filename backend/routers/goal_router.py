from typing import Optional, List

from fastapi import APIRouter, Depends, Query, HTTPException

from dependencies import get_current_user_id
from services.goal_service import (
    create_goal,
    get_goal_by_id,
    get_user_goals,
    update_goal,
    add_amount_to_goal,
    delete_goal,
    GoalCreate,
    GoalUpdate,
    GoalResponse,
)

goal_router = APIRouter(prefix='/api/v1/goal')


@goal_router.post("/", response_model=GoalResponse)
async def create_goal_endpoint(
    data: GoalCreate,
    user_id: int = Depends(get_current_user_id),
):
    return await create_goal(user_id, data)


@goal_router.get("/", response_model=List[GoalResponse])
async def get_goals(
    is_completed: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
    user_id: int = Depends(get_current_user_id),
):
    return await get_user_goals(user_id, is_completed)


@goal_router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    user_id: int = Depends(get_current_user_id),
):
    goal = await get_goal_by_id(goal_id, user_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@goal_router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal_endpoint(
    goal_id: int,
    data: GoalUpdate,
    user_id: int = Depends(get_current_user_id),
):
    return await update_goal(goal_id, user_id, data)


@goal_router.post("/{goal_id}/add-amount", response_model=GoalResponse)
async def add_amount_endpoint(
    goal_id: int,
    amount: float = Query(..., ge=0, description="Сумма для добавления"),
    user_id: int = Depends(get_current_user_id),
):
    return await add_amount_to_goal(goal_id, user_id, amount)


@goal_router.delete("/{goal_id}")
async def delete_goal_endpoint(
    goal_id: int,
    user_id: int = Depends(get_current_user_id),
):
    await delete_goal(goal_id, user_id)
    return {"message": "Goal deleted successfully"}
