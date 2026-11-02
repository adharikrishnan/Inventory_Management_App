

from typing import Optional
from pydantic import BaseModel
from schema.user import User


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: str
    last_name: str 
    disabled: bool = False

    def __init__(self, user: User):
        super().__init__(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            disabled=user.disabled
        )


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserDto(UserBase):
    id: int
    password_hash: str

    def __init__(self, user: User):
        super().__init__(user)
        self.id = user.id
        self.password_hash = user.password_hash

