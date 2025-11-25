from sqlalchemy import Column, Float, String, Date, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from base import Base
import enum


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255))
    date = Column(Date, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    tags = Column(String(255))
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
