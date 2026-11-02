import secrets
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends
from repository.user_repository import UserRepository
from schema.user import RefreshToken, User
from settings.settings import Settings, get_settings
from pwdlib import PasswordHash

class AuthService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(UserRepository),
        settings: Settings = Depends(get_settings),
    ):
        self.user_repo = user_repo
        self.settings = settings
        self.password_hasher = PasswordHash.recommended()
                
    async def login_user(self, username: str, password: str) -> Optional[tuple[str, str]]:
        user = await self.user_repo.get_user(username)
        if user and await self.verify_password(password, user.hashed_password):
            return await self.generate_tokens_for_user(user)
        return None
        
    async def hash_password(self, password: str) -> str:
        return await asyncio.to_thread(self.password_hasher.hash, password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return await asyncio.to_thread(
            self.password_hasher.verify, plain_password, hashed_password
        )
    
    def create_access_token(
        self,
        user_id: int,
        email: Optional[str] = None,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Create a JWT access token containing user id and email."""
        now = datetime.now(timezone.utc)
        expire = now + (
            expires_delta
            or timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        payload = {
            "sub": str(user_id),
            "user_id": user_id,
            "email": email,
            "iat": now,
            "exp": expire,
        }
        token = jwt.encode(
            payload,
            self.settings.SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM,
        )
        return token

    async def create_refresh_token(
        self,
        user_id: int,
        expires_delta: Optional[timedelta] = None,
    ) -> RefreshToken:
        """Generate a secure refresh token and save it to the database."""
        token_str = secrets.token_urlsafe(64)
        now = datetime.now(timezone.utc)
        expires_at = now + (
            expires_delta
            or timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        refresh_token = RefreshToken(
            token=token_str,
            user_id=user_id,
            expires_at=expires_at,
            created_at=now,
            revoked=False,
        )
        return await self.user_repo.save_refresh_token(refresh_token)

    async def generate_tokens_for_user(
        self,
        user: User,
    ) -> tuple[str, str]:
        access_token = self.create_access_token(user_id=user.id, email=user.email)
        refresh_token_record = await self.create_refresh_token(user_id=user.id)
        return access_token, refresh_token_record.token

