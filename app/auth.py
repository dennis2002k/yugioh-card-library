from fastapi import Depends, APIRouter, HTTPException, status, Form
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from .database import SessionDep
from .models import UserinDB
from sqlmodel import select, Session
from pwdlib import PasswordHash
import jwt

# load  secret key from env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env")


class Token(BaseModel):
    access_token: str
    token_type: str


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(session: Session, username: str):
    statement = select(UserinDB).where(UserinDB.username == username)
    return session.exec(statement).one_or_none()    


def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def authenticate_user(session: Session, username: str, passowrd: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(passowrd, user.hashed_password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


router = APIRouter()


@router.post("/token")
async def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    ## create jwt token
    token = create_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type="bearer")

@router.post("/register")
async def register_user(session: SessionDep, username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[str, Form()]):
    hashed_password = get_password_hash(password)
    new_user = UserinDB(username=username, hashed_password=hashed_password, email=email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    session.close()
