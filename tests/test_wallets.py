from fastapi.testclient import TestClient


class TestWalletCreation:
    def test_create_wallet_success(self, client: TestClient, test_user: dict) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        response = client.post("/wallets", headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert "address" in data
        assert "balance_btc" in data
        assert "balance_usd" in data

    def test_create_wallet_requires_api_key(self, client: TestClient) -> None:
        response = client.post("/wallets")
        assert response.status_code == 422

    def test_create_wallet_initial_balance(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        response = client.post("/wallets", headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["balance_btc"] == 1.0

    def test_create_wallet_limit_three_per_user(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        for _ in range(3):
            response = client.post("/wallets", headers=headers)
            assert response.status_code == 201

        response = client.post("/wallets", headers=headers)
        assert response.status_code == 400
        assert "Maximum wallet limit reached" in response.json()["detail"]


class TestWalletRetrieval:
    def test_get_wallet_success(self, client: TestClient, test_user: dict) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        create_response = client.post("/wallets", headers=headers)
        wallet = create_response.json()

        response = client.get(f"/wallets/{wallet['address']}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["address"] == wallet["address"]
        assert data["balance_btc"] == 1.0

    def test_get_wallet_requires_api_key(self, client: TestClient) -> None:
        response = client.get("/wallets/fake-address")
        assert response.status_code == 422

    def test_get_wallet_not_found(self, client: TestClient, test_user: dict) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        response = client.get("/wallets/nonexistent-address", headers=headers)
        assert response.status_code == 404

    def test_get_wallet_unauthorized_user(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        create_response = client.post("/wallets", headers=headers)
        wallet = create_response.json()

        other_user_response = client.post("/users")
        other_user = other_user_response.json()
        other_headers = {"X-API-KEY": other_user["api_key"]}

        response = client.get(f"/wallets/{wallet['address']}", headers=other_headers)
        assert response.status_code == 403

