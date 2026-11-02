from fastapi.params import Depends
from repository.user_repository import UserRepository
from schema.user import User

class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def get_user(self, username: str) -> User:
        return await self.user_repository.get_user(username)

    async def get_user_count(self) -> int:
        return await self.user_repository.get_user_count()