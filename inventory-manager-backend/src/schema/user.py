
from typing import Optional
from pydantic import BaseModel


class user(BaseModel):
    id: int
    username: str
    password_hash: str
    email: Optional[str] = None
    first_name: str
    last_name: str
    disabled: bool