from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from typing import List, Dict, Optional, List
from sqlalchemy import JSON, Column, Text 
from pydantic import BaseModel


class CardSetLink(SQLModel, table=True):
    card_id: int | None = Field(foreign_key="card.id", primary_key=True, index=True)
    set_id: int | None = Field(foreign_key="cardset.id", primary_key=True, index=True)

    # card: "Card" = Relationship(back_populates="sets")
    # cardset: "CardSet" = Relationship(back_populates="cards")


class Card(SQLModel, table=True):
    id: int = Field( primary_key=True)
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
    card_sets:  str = Field(default="[]", sa_column=Column(Text))
    card_images:  str = Field(default="[]", sa_column=Column(Text))
    card_prices:  str = Field(default="[]")

    sets: List["CardSet"] = Relationship(
        back_populates="cards",
        link_model=CardSetLink
    )

    model_config = {"from_attributes": True}


class CardSet(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    cards: List[Card] = Relationship(
        back_populates="sets",
        link_model=CardSetLink
    )


class CardRead(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True)
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
    card_sets:  str = Field(default="[]", sa_column=Column(Text))
    card_images:  str = Field(default="[]", sa_column=Column(Text))
    card_prices:  str = Field(default="[]")


    model_config = {"from_attributes": True}



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


