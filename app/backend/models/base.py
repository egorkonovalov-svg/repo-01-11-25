from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from pydantic import BaseModel


class Base(BaseModel):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
