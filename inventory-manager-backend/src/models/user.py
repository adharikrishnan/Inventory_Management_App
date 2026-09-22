

from typing import Optional
from pydantic import BaseModel
from schema.user import user


class user_base(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: str
    last_name: str 
    disabled: bool = False

    def __init__(self, user: user):
        super().__init__(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            disabled=user.disabled
        )


class user_create(user_base):
    password: str

class user_login():
    username: str
    password: str

class user_dto(user_base):
    id: int
    password_hash: str

    def __init__(self, user: user):
        super().__init__(user)
        self.id = user.id
        self.password_hash = user.password_hash

