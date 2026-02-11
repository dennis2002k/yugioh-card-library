from fastapi import FastAPI, Depends, Query
from typing import Annotated
from .database import SessionDep, create_db_and_tables
from app import users
from app import auth
from app import utilities
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager
from .config import settings
# from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables() 
    yield


app = FastAPI(lifespan=lifespan, title=settings.app_name)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(utilities.router)

@app.get("/")
def root():
    return {
        "env_debug": settings.debug,
        "db": settings.database_url
    }

origins = [
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






