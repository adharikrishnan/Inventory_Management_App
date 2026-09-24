from repository.user_repository import user_repository
from schema.user import user

class user_service():
    def __init__(self, user_repository: user_repository):
        self.user_repository = user_repository

    async def get_user(self, username: str) -> user:
        return await self.user_repository.get_user(username)