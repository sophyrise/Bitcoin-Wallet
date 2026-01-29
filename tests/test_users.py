from fastapi.testclient import TestClient


class TestUserRegistration:
    def test_register_user_success(self, client: TestClient) -> None:
        response = client.post("/users")
        assert response.status_code == 201
        data = response.json()
        assert "api_key" in data
        assert isinstance(data["api_key"], str)
        assert len(data["api_key"]) > 0

    def test_register_user_returns_api_key(self, client: TestClient) -> None:
        response = client.post("/users")
        assert response.status_code == 201
        data = response.json()
        api_key = data["api_key"]
        assert api_key is not None
        assert len(api_key) > 20

    def test_api_key_is_unique(self, client: TestClient) -> None:
        response1 = client.post("/users")
        response2 = client.post("/users")

        assert response1.status_code == 201
        assert response2.status_code == 201

        api_key1 = response1.json()["api_key"]
        api_key2 = response2.json()["api_key"]

        assert api_key1 != api_key2

