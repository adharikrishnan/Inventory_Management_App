
from contextlib import asynccontextmanager
from http.client import HTTPException
import logging
from typing import Optional
from fastapi.concurrency import asynccontextmanager
from service.auth_service import AuthService
from fastapi import Cookie, Depends, FastAPI, FastAPI, logger, status
from mock.mock_data import setup_local_database
from settings.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    _settings = get_settings()
    logger = logging.getLogger("uvicorn.error")
    if _settings.ENVIRONMENT == "development":
        try:
            await setup_local_database()
        except Exception as e:
            logger.exception("Failed to initialize database during startup: %s", e)
    yield

async def check_auth(access_token: Optional[str] = Cookie(None), auth_service: AuthService = Depends(AuthService)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    payload = auth_service.verify_access_token(access_token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return {"user_id": user_id}