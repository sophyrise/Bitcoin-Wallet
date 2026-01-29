import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import Database


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
def test_wallet(client, test_user):
    pass


@pytest.fixture
def admin_headers():
    pass

