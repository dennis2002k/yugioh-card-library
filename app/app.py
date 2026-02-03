from fastapi import FastAPI, Depends, Query
from typing import Annotated
from .database import SessionDep, create_db_and_tables
from app import users
from app import auth
from app import utilities
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os



app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(utilities.router)

IMAGE_PATH = "images"

if os.path.exists(IMAGE_PATH):
    app.mount("/images", StaticFiles(directory=IMAGE_PATH), name="images")
else:
    print(f"Warning: {IMAGE_PATH} directory not found. Static files not mounted.")



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


