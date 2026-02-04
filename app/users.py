from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, Body, Path, Query
from pydantic import BaseModel
from .auth import oauth2_scheme
from sqlmodel import Field, SQLModel, Session, select, func
from .models import User, UserinDB, Card, CardUserLink, CardFilter, CardRead
import jwt
from jwt.exceptions import InvalidTokenError
from .database import SessionDep
from dotenv import load_dotenv
import os
from .utilities import search_card

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


@router.get("/me/library", response_model=list[CardRead])
async def get_all_cards(session: SessionDep, curr_user: Annotated[User, Depends(get_current_active_user)]):
    cards = session.exec(
        select(Card, CardUserLink.quantity, CardUserLink.set_code, CardUserLink.set_rarity_code)
        .join(CardUserLink)
        .where(CardUserLink.user_id == curr_user.id)
    ).all()

    output = []
    for card_obj, qty, set, rarity in cards:
        # 2. Convert the Card ORM object to a dict
        card_data = card_obj.model_dump()
        
        # 3. Inject the quantity from the join into the data
        card_data["quantity"] = qty
        card_data["set_code"] = set
        card_data["set_rarity_code"] = rarity
        
        # 4. Create a CardRead instance (this triggers your validators!)
        output.append(CardRead(**card_data))


    return output

@router.post("/me/library/add")
async def add_card_to_library(
    session: SessionDep, 
    card: Annotated[Card, Body()], 
    curr_user: Annotated[User, Depends(get_current_active_user)]):


    #check if given card is valid in all cards database
    db_card = session.get(Card, card.id)
    if not db_card:
        raise HTTPException(
            status_code=404,
            detail="Card does not exist"
        )

    statement = select(CardUserLink).where(CardUserLink.user_id == curr_user.id)
    statement = statement.where(CardUserLink.card_id == card.id)
    card_in_lib = session.exec(statement).one_or_none()

    if card_in_lib:
        card_in_lib.quantity += 1
        session.add(card_in_lib)
        session.commit()
        session.refresh(card_in_lib)
        print("Updated card in library: ", card_in_lib)
    else:
        new_card = CardUserLink(user_id=curr_user.id, card_id=card.id, quantity=1)
        session.add(new_card)
        session.commit()
        session.refresh(new_card)
        print("Added card in library: ", card)
    return {"success": True, "message": "Card added"}

@router.delete("/me/library/delete/{card_id}")
async def delete_card_from_library(
    session: SessionDep, 
    card_id: Annotated[int, Path()],
    curr_user: Annotated[User, Depends(get_current_active_user)],
    remove_all: Annotated[bool | None, Query()] = False,):

    statement = select(CardUserLink).where(CardUserLink.user_id == curr_user.id)
    statement = statement.where(CardUserLink.card_id == card_id)
    card_in_lib = session.exec(statement).one_or_none()

    if card_in_lib:
        if not remove_all and  card_in_lib.quantity > 1:
            card_in_lib.quantity -= 1
            session.add(card_in_lib)
            session.commit()
            print("Removed 1 copy of card in library: ", card_in_lib)
        else:
            session.delete(card_in_lib)
            session.commit()
            print("Removed all copies of card in library: ", card_in_lib)
    else:
        raise HTTPException(
            status_code=404,
            detail="Card not found in user's library"
        )
    return {"success": True, "message": "Card removed"}
    

@router.get("/me/library/search", response_model=list[CardRead])
async def search_card_library(
    session: SessionDep,
    curr_user: Annotated[User, Depends(get_current_active_user)],
    filters: CardFilter = Depends()):

    #TODO swamp order to be faster
    statement = search_card(filters, in_library=True)
    statement = statement.join(CardUserLink).where(CardUserLink.user_id == curr_user.id)

    cards = session.exec(statement).all()

    output = []
    for card_obj, qty, set, rarity in cards:
        # 2. Convert the Card ORM object to a dict
        card_data = card_obj.model_dump()
        
        # 3. Inject the quantity from the join into the data
        card_data["quantity"] = qty
        card_data["set_code"] = set
        card_data["set_rarity_code"] = rarity
        
        # 4. Create a CardRead instance (this triggers your validators!)
        output.append(CardRead(**card_data))


    return output


@router.get("/_debug_openapi")
async def get_card_count(session: SessionDep):
    # This creates: SELECT count(card.id) FROM card
    statement = select(func.count()).select_from(Card)
    results = session.exec(statement)
    return results.one()