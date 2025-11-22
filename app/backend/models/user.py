from sqlalchemy import Column, String, Boolean, LargeBinary, Integer
from sqlalchemy.orm import relationship
from base import Base


class User(Base):
    __tablename__ = "users"
    UserName = Column(String, unique=True)
    Email = Column(String())
    PasswordHash = Column(LargeBinary())
    # Password = Column(String(), nullable=False)
    Name = Column(String())
    # Age = Column(Integer())