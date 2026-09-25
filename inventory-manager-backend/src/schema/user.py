from typing import Optional
from sqlalchemy import Column, Integer
from models import Base

class user(Base):
    __schema__ = "im"
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(str, unique=True, index=True)
    password_hash = Column(str)
    email = Column(Optional[str], default=None)
    first_name = Column(str)
    last_name = Column(str)
    disabled = Column(bool, default=False)