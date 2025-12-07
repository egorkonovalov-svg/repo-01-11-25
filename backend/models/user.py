from sqlalchemy import Column, String, LargeBinary, Integer
from sqlalchemy.orm import relationship
from models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    UserName = Column(String, unique=True)
    Email = Column(String())
    PasswordHash = Column(LargeBinary())
    Name = Column(String())
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    categories = relationship("Category", back_populates="user")