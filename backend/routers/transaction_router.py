import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from datetime import date
from services.transaction_service import (
    create_transaction,
    get_transaction_by_id,
    get_user_transactions,
    get_transactions_summary,
    update_transaction,
    delete_transaction,
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)
from models.transaction import TransactionType
from dependencies import get_current_user_id

transaction_router = APIRouter(prefix='/api/v1/transaction')


@transaction_router.post("/", response_model=TransactionResponse)
async def create_transaction_endpoint(
    data: TransactionCreate,
    user_id: int = Depends(get_current_user_id)
):
    """Создать новую транзакцию"""
    return await create_transaction(user_id, data)


@transaction_router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    start_date: Optional[date] = Query(None, description="Начальная дата"),
    end_date: Optional[date] = Query(None, description="Конечная дата"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    type: Optional[TransactionType] = Query(None, description="Тип транзакции"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    offset: int = Query(0, ge=0, description="Смещение"),
    user_id: int = Depends(get_current_user_id)
):
    """Получить транзакции пользователя с фильтрами"""
    return await get_user_transactions(
        user_id, start_date, end_date, category_id, type, limit, offset
    )


@transaction_router.get("/summary")
async def get_summary(
    start_date: Optional[date] = Query(None, description="Начальная дата"),
    end_date: Optional[date] = Query(None, description="Конечная дата"),
    user_id: int = Depends(get_current_user_id)
):
    """Получить сводку по транзакциям (доходы, расходы, баланс)"""
    return await get_transactions_summary(user_id, start_date, end_date)


@transaction_router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Получить транзакцию по ID"""
    transaction = await get_transaction_by_id(transaction_id, user_id)
    if not transaction:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@transaction_router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction_endpoint(
    transaction_id: int,
    data: TransactionUpdate,
    user_id: int = Depends(get_current_user_id)
):
    """Обновить транзакцию"""
    return await update_transaction(transaction_id, user_id, data)


@transaction_router.delete("/{transaction_id}")
async def delete_transaction_endpoint(
    transaction_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """Удалить транзакцию"""
    await delete_transaction(transaction_id, user_id)
    return {"message": "Transaction deleted successfully"}
