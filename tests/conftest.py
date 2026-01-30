import pytest
from fastapi.testclient import TestClient

from src.config import settings
from src.database import Database
from src.main import app


@pytest.fixture
def test_database():
    db = Database(":memory:")
    db.create_tables()
    yield db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user(client):
    response = client.post("/users")
    return response.json()


@pytest.fixture
def test_wallet(client: TestClient, test_user: dict) -> dict:
    headers = {"X-API-KEY": test_user["api_key"]}
    response = client.post("/wallets", headers=headers)
    return response.json()


@pytest.fixture
def admin_headers():
    return {"X-API-KEY": settings.admin_api_key}

