from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from typing import List, Dict, Optional, List
from sqlalchemy import JSON, Column, Text 
from pydantic import BaseModel,  field_validator
import json


class CardSetLink(SQLModel, table=True):
    card_id: int | None = Field(foreign_key="card.id", primary_key=True, index=True)
    set_id: int | None = Field(foreign_key="cardset.id", primary_key=True, index=True)

    # card: "Card" = Relationship(back_populates="sets")
    # cardset: "CardSet" = Relationship(back_populates="cards")

class CardBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    type: str = Field(default=None, index=True) 
    frameType: str | None = Field(default=None, index=True) 
    desc: str | None = Field(default=None,  sa_column=Column(Text))
    pend_desc: str | None = Field(default=None,  sa_column=Column(Text))
    atk: int | None = Field(default=None, index=True) 
    defense: int | None = Field(default=None, index=True)
    level: int | None = Field(default=None, index=True) 
    race: str | None = Field(default=None, index=True) 
    attribute: str | None = Field(default=None, index=True)
    scale: int | None = Field(default=None, index=True) 
    archetype: str | None = Field(default=None, index=True)
    link_rating: int | None = Field(default=None, index=True)
    link_arrows: str | None = Field(default=None, index=True)


    
class CardRead(CardBase):
    card_sets:  list[dict] | None = Field(default=[])
    card_images:  dict | None = Field(default=[])
    card_prices:  list[dict] | None = Field(default=[])
    quantity: int | None = 1

    @field_validator("card_sets", "card_images", "card_prices", mode="before")
    @classmethod
    def transform_images(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v


class Card(CardBase, table=True):
    card_sets:  str = Field(default="[]", sa_column=Column(Text))
    card_images:  str = Field(default="[]", sa_column=Column(Text))
    card_prices:  str = Field(default="[]")

    sets: List["CardSet"] = Relationship(
        back_populates="cards",
        link_model=CardSetLink
    )




class CardSet(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    cards: List[Card] = Relationship(
        back_populates="sets",
        link_model=CardSetLink
    )


class CardFilter(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, index=True)
    type: str | None = Field(default=None, index=True) 
    frameType: str | None = Field(default=None, index=True) 
    desc: str | None = Field(default=None,  sa_column=Column(Text))
    pend_desc: str | None = Field(default=None,  sa_column=Column(Text))
    min_atk: int | None = Field(default=None, index=True, ge=0) 
    max_atk: int | None = Field(default=None, index=True, ge=0)
    atk: int | None = Field(default=None, index=True, ge=0)
    min_defense: int | None = Field(default=None, index=True, ge=0)
    max_defense: int | None = Field(default=None, index=True, ge=0)
    defense: int | None = Field(default=None, index=True, ge=0)
    min_level: int | None = Field(default=None, index=True, ge=0, le=12) 
    max_level: int | None = Field(default=None, index=True, ge=0, le=12) 
    level: int | None = Field(default=None, index=True, ge=0, le=12)
    race: str | None = Field(default=None, index=True) 
    attribute: str | None = Field(default=None, index=True)
    scale: int | None = Field(default=None, index=True) 
    archetype: str | None = Field(default=None, index=True)
    link_rating: int | None = Field(default=None, index=True)
    link_arrows: str | None = Field(default=None, index=True)


class User(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    is_active: bool = True

class UserinDB(User, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str

class CardUserLink(SQLModel, table=True):
    card_id: int | None = Field(foreign_key="card.id", primary_key=True, index=True)
    user_id: int | None = Field(foreign_key="userindb.id", primary_key=True, index=True)
    quantity: int | None

