from models.goal import Goal
from database import async_session_maker
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from fastapi import HTTPException


class GoalCreate(BaseModel):
    name: str
    target_amount: float
    deadline: Optional[date] = None
    description: Optional[str] = None


class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[date] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class GoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    current_amount: float
    deadline: Optional[date]
    description: Optional[str]
    is_completed: bool
    user_id: int

    class Config:
        from_attributes = True


async def create_goal(user_id: int, data: GoalCreate) -> Goal:
    """Создать новую цель"""
    async with async_session_maker() as session:
        new_goal = Goal(
            name=data.name,
            target_amount=data.target_amount,
            deadline=data.deadline,
            description=data.description,
            user_id=user_id,
            current_amount=0.0,
            is_completed=False
        )
        session.add(new_goal)
        await session.commit()
        await session.refresh(new_goal)
        return new_goal


async def get_goal_by_id(goal_id: int, user_id: int) -> Optional[Goal]:
    """Получить цель по ID"""
    async with async_session_maker() as session:
        query = select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id
        )
        result = await session.execute(query)
        return result.scalars().first()


async def get_user_goals(
    user_id: int,
    is_completed: Optional[bool] = None
) -> List[Goal]:
    """Получить все цели пользователя"""
    async with async_session_maker() as session:
        query = select(Goal).where(Goal.user_id == user_id)
        
        if is_completed is not None:
            query = query.where(Goal.is_completed == is_completed)
        
        query = query.order_by(Goal.deadline.asc().nulls_last())
        result = await session.execute(query)
        return list(result.scalars().all())


async def update_goal(goal_id: int, user_id: int, data: GoalUpdate) -> Goal:
    """Обновить цель"""
    async with async_session_maker() as session:
        query = select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id
        )
        result = await session.execute(query)
        goal = result.scalars().first()
        
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        if data.name is not None:
            goal.name = data.name
        if data.target_amount is not None:
            goal.target_amount = data.target_amount
        if data.current_amount is not None:
            goal.current_amount = data.current_amount
            # Автоматически помечаем как выполненную, если достигнута цель
            if goal.current_amount >= goal.target_amount:
                goal.is_completed = True
        if data.deadline is not None:
            goal.deadline = data.deadline
        if data.description is not None:
            goal.description = data.description
        if data.is_completed is not None:
            goal.is_completed = data.is_completed
        
        await session.commit()
        await session.refresh(goal)
        return goal


async def add_amount_to_goal(goal_id: int, user_id: int, amount: float) -> Goal:
    """Добавить сумму к текущему прогрессу цели"""
    async with async_session_maker() as session:
        query = select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id
        )
        result = await session.execute(query)
        goal = result.scalars().first()
        
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        goal.current_amount += amount
        if goal.current_amount >= goal.target_amount:
            goal.is_completed = True
        
        await session.commit()
        await session.refresh(goal)
        return goal


async def delete_goal(goal_id: int, user_id: int) -> bool:
    """Удалить цель"""
    async with async_session_maker() as session:
        query = select(Goal).where(
            Goal.id == goal_id,
            Goal.user_id == user_id
        )
        result = await session.execute(query)
        goal = result.scalars().first()
        
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        await session.delete(goal)
        await session.commit()
        return True

