from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Body, Path, Query
from pydantic import BaseModel
from .auth import oauth2_scheme
from sqlmodel import Field, SQLModel, Session, select, col
from .models import User, UserinDB, Card, CardUserLink, CardFilter, CardRead
import jwt
from jwt.exceptions import InvalidTokenError
from .database import SessionDep
from dotenv import load_dotenv
import os

router = APIRouter()

def search_card(filters: CardFilter = Depends()):

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
    
    return statement



@router.get("/card/search", response_model=list[CardRead])
async def seacrh_card_db(session: SessionDep, filters: CardFilter = Depends()):
    
    statement = search_card(filters)

    return session.exec(statement).all()
