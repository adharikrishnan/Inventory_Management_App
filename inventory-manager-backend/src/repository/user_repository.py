from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from schema.user import User, RefreshToken
from database.database import get_db

class UserRepository:
    def __init__(self, db_session: AsyncSession = Depends(get_db)):
        self.db_session = db_session

    async def get_user(self, username: str) -> User | None:
        stm = select(User).where(User.username == username)
        result = await self.db_session.execute(stm)
        return result.scalar_one_or_none()

    async def get_user_count(self) -> int:
        stm = select(func.count(User.id))
        result = await self.db_session.execute(stm)
        return result.scalar_one()

    async def save_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db_session.add(refresh_token)
        await self.db_session.commit()
        await self.db_session.refresh(refresh_token)
        return refresh_token

    async def get_refresh_token(self, token: str) -> RefreshToken | None:
        stm = select(RefreshToken).where(RefreshToken.token == token)
        result = await self.db_session.execute(stm)
        return result.scalar_one_or_none()