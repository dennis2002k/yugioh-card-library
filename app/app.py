from fastapi import FastAPI, Depends, Query
from typing import Annotated
from sqlalchemy import create_engine, text,  select
from sqlmodel import SQLModel, Field, create_engine, Session, col
from dotenv import load_dotenv
from ..app.models import CardRead, Card, CardFilter
import os
from fastapi.encoders import jsonable_encoder




# load database url from env variable
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

# connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.get("/card/search", response_model=list[CardRead])
async def search_card( session: SessionDep, filters: CardFilter = Depends()):

    operators = {
        "min": "__ge__",
        "max": "__le__"
    }
    statement = select(Card)
    filter_data = filters.model_dump(exclude_none=True)
    print(filter_data)

    for key, value in filter_data.items():
        if "_" in key and key.split("_")[0] in operators:
            suffix, field_name = key.rsplit("_", 1)
            column = getattr(Card, field_name)
            operator = operators[suffix]
            statement = statement.where(getattr(column, operator)(value))
        else:
            column = getattr(Card, key)
            if isinstance(value, str):
                # if key == "link_arrows": ## TODO create a function to get data of this column , make the string to list and then check
                #     statement = statement.where(getattr(Card, key) == value)
                # else:
                statement = statement.where(col(column).ilike(f"%{value}%"))
            else:
                statement = statement.where(column == value)
    
    return session.exec(statement).scalars().all()

