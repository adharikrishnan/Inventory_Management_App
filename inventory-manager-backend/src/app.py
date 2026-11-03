from contextlib import asynccontextmanager
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from mock.mock_data import setup_local_database
from settings.settings import get_settings
from service.user_service import UserService
from service.auth_service import AuthService
from models.user import UserLogin, TokenResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.ENVIRONMENT == "development":
        try:
            await setup_local_database()
        except Exception as e:
            print(f"Could not connect to database during startup: {e}")
            raise e
    yield

app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/login", response_model=TokenResponse)
async def login(
    request: UserLogin,
    auth_service: AuthService = Depends(AuthService),
):
    result = await auth_service.login_user(request.username, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token, refresh_token = result
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

@app.get("/users/count")
async def get_user_count(user_service: UserService = Depends(UserService)):
    count = await user_service.get_user_count()
    return {"user_count": count}