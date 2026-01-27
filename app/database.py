from sqlalchemy import create_engine
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
import os


# load database url from env variable
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

# connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

