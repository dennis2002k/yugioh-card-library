import requests
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv
import os
from pydantic import create_model
from app.models import *
import json

url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

# load database url from env variable
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

engine = create_engine(DATABASE_URL)

# # get cards from ygoprodeck api
# print("Fetching cards from Yu-Gi-Oh API...\n")
# response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
# response.raise_for_status()
# cards = response.json()["data"]

# length = len(cards)
# print(f"number of cards: {length}\n")

response = requests.get(f"{url}?name=Ally of Justice Cycle Reader")
response.raise_for_status()
card = response.json()["data"]
for attr, value in card[0].items():
    print(attr + " ")
    print(value)
    print("\n")



