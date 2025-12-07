from models.transaction import Transaction, TransactionType
from database import async_session_maker
from sqlalchemy import select, and_, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from fastapi import HTTPException


class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    date: date
    type: TransactionType
    category_id: int
    tags: Optional[str] = None


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None
    type: Optional[TransactionType] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    date: date
    type: TransactionType
    user_id: int
    category_id: int
    tags: Optional[str]

    class Config:
        from_attributes = True


async def create_transaction(user_id: int, data: TransactionCreate) -> Transaction:
    """Создать новую транзакцию"""
    async with async_session_maker() as session:
        new_transaction = Transaction(
            amount=data.amount,
            description=data.description,
            date=data.date,
            type=data.type,
            category_id=data.category_id,
            user_id=user_id,
            tags=data.tags
        )
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
        return new_transaction


async def get_transaction_by_id(transaction_id: int, user_id: int) -> Optional[Transaction]:
    """Получить транзакцию по ID"""
    async with async_session_maker() as session:
        query = select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        result = await session.execute(query)
        return result.scalars().first()


async def get_user_transactions(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    type: Optional[TransactionType] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Transaction]:
    """Получить транзакции пользователя с фильтрами"""
    async with async_session_maker() as session:
        query = select(Transaction).where(Transaction.user_id == user_id)
        
        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)
        if category_id:
            query = query.where(Transaction.category_id == category_id)
        if type:
            query = query.where(Transaction.type == type)
        
        query = query.order_by(Transaction.date.desc()).limit(limit).offset(offset)
        result = await session.execute(query)
        return list(result.scalars().all())


async def get_transactions_summary(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> dict:
    """Получить сводку по транзакциям (доходы и расходы)"""
    async with async_session_maker() as session:
        query = select(
            Transaction.type,
            func.sum(Transaction.amount).label('total')
        ).where(Transaction.user_id == user_id)
        
        if start_date:
            query = query.where(Transaction.date >= start_date)
        if end_date:
            query = query.where(Transaction.date <= end_date)
        
        query = query.group_by(Transaction.type)
        result = await session.execute(query)
        
        summary = {"income": 0.0, "expense": 0.0}
        for row in result.all():
            if row.type == TransactionType.INCOME:
                summary["income"] = float(row.total or 0)
            elif row.type == TransactionType.EXPENSE:
                summary["expense"] = float(row.total or 0)
        
        summary["balance"] = summary["income"] - summary["expense"]
        return summary


async def update_transaction(transaction_id: int, user_id: int, data: TransactionUpdate) -> Transaction:
    """Обновить транзакцию"""
    async with async_session_maker() as session:
        query = select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        result = await session.execute(query)
        transaction = result.scalars().first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        if data.amount is not None:
            transaction.amount = data.amount
        if data.description is not None:
            transaction.description = data.description
        if data.date is not None:
            transaction.date = data.date
        if data.type is not None:
            transaction.type = data.type
        if data.category_id is not None:
            transaction.category_id = data.category_id
        if data.tags is not None:
            transaction.tags = data.tags
        
        await session.commit()
        await session.refresh(transaction)
        return transaction


async def delete_transaction(transaction_id: int, user_id: int) -> bool:
    """Удалить транзакцию"""
    async with async_session_maker() as session:
        query = select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user_id
        )
        result = await session.execute(query)
        transaction = result.scalars().first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        await session.delete(transaction)
        await session.commit()
        return True

