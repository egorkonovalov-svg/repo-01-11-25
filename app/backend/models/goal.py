from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from base import BaseModel


class Goal(BaseModel):
    __tablename__ = "goals"

    name = Column(String(100), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(Date)
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    color = Column(String(7), default="#3498db")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="goals")
