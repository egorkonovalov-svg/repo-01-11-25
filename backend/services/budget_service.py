from typing import Optional, List
from datetime import date

from sqlalchemy import select
from pydantic import BaseModel
from fastapi import HTTPException

from models.budget import Budget, BudgetPeriod
from database import async_session_maker


class BudgetCreate(BaseModel):
    name: str
    amount: float
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    start_date: date
    end_date: Optional[date] = None
    category_id: Optional[int] = None
    is_active: bool = True


class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    period: Optional[BudgetPeriod] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class BudgetResponse(BaseModel):
    id: int
    name: str
    amount: float
    period: BudgetPeriod
    start_date: date
    end_date: Optional[date]
    is_active: bool
    user_id: int
    category_id: Optional[int]

    class Config:
        from_attributes = True


async def create_budget(user_id: int, data: BudgetCreate) -> Budget:
    async with async_session_maker() as session:
        new_budget = Budget(
            name=data.name,
            amount=data.amount,
            period=data.period,
            start_date=data.start_date,
            end_date=data.end_date,
            category_id=data.category_id,
            user_id=user_id,
            is_active=data.is_active,
        )
        session.add(new_budget)
        await session.commit()
        await session.refresh(new_budget)
        return new_budget


async def get_budget_by_id(budget_id: int, user_id: int) -> Optional[Budget]:
    async with async_session_maker() as session:
        query = select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )
        result = await session.execute(query)
        return result.scalars().first()


async def get_user_budgets(
    user_id: int,
    is_active: Optional[bool] = None,
    category_id: Optional[int] = None,
) -> List[Budget]:
    async with async_session_maker() as session:
        query = select(Budget).where(Budget.user_id == user_id)

        if is_active is not None:
            query = query.where(Budget.is_active == is_active)
        if category_id is not None:
            query = query.where(Budget.category_id == category_id)

        query = query.order_by(Budget.start_date.desc())
        result = await session.execute(query)
        return list(result.scalars().all())


async def update_budget(budget_id: int, user_id: int, data: BudgetUpdate) -> Budget:
    async with async_session_maker() as session:
        query = select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )
        result = await session.execute(query)
        budget = result.scalars().first()

        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")

        update_fields = data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(budget, field, value)

        await session.commit()
        await session.refresh(budget)
        return budget


async def delete_budget(budget_id: int, user_id: int) -> bool:
    async with async_session_maker() as session:
        query = select(Budget).where(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )
        result = await session.execute(query)
        budget = result.scalars().first()

        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")

        await session.delete(budget)
        await session.commit()
        return True
