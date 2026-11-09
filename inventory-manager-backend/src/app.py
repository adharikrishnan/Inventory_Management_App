import logging
from fastapi import Depends, FastAPI, HTTPException, Response, status
from settings.settings import get_settings
from service.user_service import UserService
from service.auth_service import AuthService
from models.user import UserLogin
from dependencies import check_auth, lifespan
from middleware import setup_cors

_settings = get_settings()
    
app = FastAPI(
    lifespan=lifespan,
    debug=_settings.DEBUG.lower() == "true",
    title="Inventory Manager API",
    version="1.0.0",
)

setup_cors(app, _settings)
    
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/login")
async def login(
    request: UserLogin,
    response: Response,
    auth_service: AuthService = Depends(AuthService)
):
    logger = logging.getLogger("uvicorn.error")
    try:
        result = await auth_service.login_user(request.username, request.password)
    except Exception as e:
        logger.exception("Error during login")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
       
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token, refresh_token = result
    auth_service.set_cookies(response, access_token, refresh_token)
    return { "message": "Login successful" }


@app.get("/users/count")
async def get_user_count(current_user: dict = Depends(check_auth),
                        user_service: UserService = Depends(UserService)):
    count = await user_service.get_user_count()
    return {"user_count": count}