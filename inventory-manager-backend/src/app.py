from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/login")
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}