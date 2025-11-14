import enum
from sqlalchemy import Column, String, Text, Enum, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from base import Base


class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Base):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(Enum(TransactionType), nullable=False)
    color = Column(String(7), default="#000000")
    icon = Column(String(50))
    is_default = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")
