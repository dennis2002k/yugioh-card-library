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
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(utilities.router)

app.mount("/images", StaticFiles(directory="images"), name="images")


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


