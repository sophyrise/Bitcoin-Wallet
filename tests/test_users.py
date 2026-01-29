import pytest
from fastapi.testclient import TestClient


class TestUserRegistration:
    def test_register_user_success(self, client: TestClient) -> None:
        pass

    def test_register_user_returns_api_key(self, client: TestClient) -> None:
        pass

    def test_api_key_is_unique(self, client: TestClient) -> None:
        pass

