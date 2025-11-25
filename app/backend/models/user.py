from sqlalchemy import Column, String, Boolean, LargeBinary, Integer
from sqlalchemy.orm import relationship
from base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    UserName = Column(String, unique=True)
    Email = Column(String())
    PasswordHash = Column(LargeBinary())
    Name = Column(String())