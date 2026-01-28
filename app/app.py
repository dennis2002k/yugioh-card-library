from fastapi import FastAPI, Depends, Query
from typing import Annotated
from sqlalchemy import create_engine, text,  select
from sqlmodel import SQLModel, Field, create_engine, Session, col
from .models import CardRead, Card, CardFilter, User, UserinDB
from fastapi.encoders import jsonable_encoder
from .database import SessionDep, create_db_and_tables
from . import users
from . import auth
from . import utilities




app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(utilities.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


