from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from .auth import oauth2_scheme
from sqlmodel import Field, SQLModel, Session, select
from .models import User, UserinDB
import jwt
from jwt.exceptions import InvalidTokenError
from .database import SessionDep
from dotenv import load_dotenv
import os

# load  secret key from env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env")


router = APIRouter()

async def get_current_user(session: SessionDep, token: Annotated[User, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = session.exec(select(UserinDB).where(UserinDB.username == username)).one_or_none()
    if not user:
        raise credentials_exception
    return user

async def get_current_active_user(curr_user: Annotated[User, Depends(get_current_user)]):
    if curr_user.is_active:
        return curr_user
    else:
        raise HTTPException(status_code=400, detail="Inactive user")


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@router.get("/me", response_model=User)
async def read_users_me(curr_user: Annotated[User, Depends(get_current_active_user)]):
    return curr_user