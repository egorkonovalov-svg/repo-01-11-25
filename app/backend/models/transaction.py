from sqlalchemy import Column, Float, String, Date, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from base import BaseModel
from category import TransactionType


class Transaction(BaseModel):
    __tablename__ = "transactions"

    amount = Column(Float, nullable=False)
    description = Column(String(255))
    date = Column(Date, nullable=False, index=True)
    type = Column(Enum(TransactionType), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    tags = Column(String(255))
    location = Column(String(255))

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
