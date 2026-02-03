import pytest
from app.models import UserinDB, Card, CardSetLink, CardUserLink
from fastapi.testclient import TestClient
from app.app import app
from app.database import get_session, create_db_and_tables
from pwdlib import PasswordHash
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import os
from sqlalchemy import inspect
from sqlalchemy.pool import StaticPool



load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env")

password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


@pytest.fixture(scope="function")
def test_session():
    test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # This keeps the data alive in memory for the whole test
    )
    
    SQLModel.metadata.create_all(test_engine)
    print(inspect(test_engine).get_table_names())
    with Session(test_engine) as session:
        yield session
        session.rollback()  # reset after each test

    SQLModel.metadata.drop_all(test_engine)


# ---------- Test Client Fixture ----------
@pytest.fixture(scope="function")
def client(test_session):
    # Override FastAPI dependency to use test session
    def get_test_session():
        yield test_session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------- Create test user ----------
def create_test_user(session):
    hashed_password = get_password_hash("testpassword")
    user = UserinDB(username="testuser", email="test@example.com", hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def create_test_cards(session):
    test_card = Card(
        id=96676583, 
        name="Blue-Eyes White Dragon",
        type="xyz mosnter"
    )
    test_card2 = Card(
        id=32061192, 
        name="Blue-Eyes White Dragon3",
        type="synchro monster"
    )
    session.add(test_card)
    session.add(test_card2)
    session.commit()


@pytest.fixture(scope="function")
def test_cards(test_session):
    create_test_cards(test_session)


# ---------- Auth Fixture ----------
@pytest.fixture(scope="function")
def test_user(test_session):
    create_test_cards(test_session)
    return create_test_user(test_session)


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}