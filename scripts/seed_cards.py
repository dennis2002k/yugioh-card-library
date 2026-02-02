import requests
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv
import os
from pydantic import create_model
from app.models import Card
import json

url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
IMAGES_PATH = "../images"


def download_image(url, size, card):
    if size == "id":
        return
    
    try:
        # response = requests.get(url)
        # response.raise_for_status()
        split_url = url.split("/")
        # os.makedirs(f"{IMAGES_PATH}/{split_url[-2]}", exist_ok=True)
        # with open(f"{IMAGES_PATH}/{split_url[-2]}/{card["id"]}.jpg", "wb") as f:
        #     f.write(response.content)
        # change cards url images to point to new images location
        card["card_images"][0][size] = f"{IMAGES_PATH}/{split_url[-2]}/{card["id"]}.jpg"
    except requests.RequestException as e:
        print(f"Skipping {url}: {e}")
        with open("logfile.txt", "w") as f:
            f.write(card.get("name"))



# create folders to hold the card images
os.makedirs(IMAGES_PATH, exist_ok=True)

# load database url from env variable
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")

# Create engine
engine = create_engine(DATABASE_URL)
# SQLModel.metadata.drop_all(engine)
# SQLModel.metadata.create_all(engine)

resp = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark Magician")
resp.raise_for_status()
card = resp.json()["data"]
print(card[0]["frameType"])


# get cards from ygoprodeck api
print("Fetching cards from Yu-Gi-Oh API...\n")
response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
response.raise_for_status()
cards = response.json()["data"]

length = len(cards)
counter = 0
for card in cards:
    counter += 1
    # get cards images
    image_urls = card["card_images"]
    print(f"Downloading Image {counter} / {length}..\n")
    for size, url in image_urls[0].items():
        download_image(url, size, card)
    # print(card)
    # save card to database
    card_to_save = Card(
        id=card["id"],
        name=card["name"],
        type=card["type"],
        frameType=card["frameType"],
        desc=card["desc"],
        pend_desc=card.get("pend_desc"),
        atk=card.get("atk"),
        defense=card.get("def"),
        level=card.get("level"),
        race=card.get("race"),
        attribute=card.get("attribute"),
        scale=card.get("scale"),
        archetype=card.get("archetype"),
        link_rating=card.get("linkval"),
        link_arrows=json.dumps(card.get("linkmarkers")),
        card_images=json.dumps(card.get("card_images")[0]),  # convert list → JSON string
        card_sets=json.dumps(card.get("card_sets")),
        card_prices=json.dumps(card.get("card_prices"))
    )
   
    # dynamicaly create model for database table
    print("Save Card to dataset..\n")
    with Session(engine) as session:
        session.add(card_to_save)
        session.commit()
    print(card)
    






