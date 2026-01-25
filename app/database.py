import requests
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv
import os
from pydantic import create_model
from app.models import *
import json


# load database url from env variable
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env")