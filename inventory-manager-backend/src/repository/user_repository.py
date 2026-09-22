from mock.mock_db import mock_users
from schema.user import user

class user_repository:
    def __init__(self):
        self.user_db = mock_users

    async def get_user(self, username: str) -> user:
        return [user for user in self.user_db if user.username == username][0]