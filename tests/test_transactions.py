from fastapi.testclient import TestClient


class TestTransactionCreation:
    def test_create_transaction_success(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        wallet1 = client.post("/wallets", headers=headers).json()
        wallet2 = client.post("/wallets", headers=headers).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.5,
        }

        response = client.post("/transactions", json=transaction_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["from_address"] == wallet1["address"]
        assert data["to_address"] == wallet2["address"]
        assert data["amount_btc"] == 0.5
        assert data["fee_btc"] == 0.0

    def test_create_transaction_requires_api_key(self, client: TestClient) -> None:
        transaction_data = {
            "from_address": "fake-address",
            "to_address": "another-fake",
            "amount_btc": 0.1,
        }
        response = client.post("/transactions", json=transaction_data)
        assert response.status_code == 422

    def test_transaction_same_user_no_fee(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        wallet1 = client.post("/wallets", headers=headers).json()
        wallet2 = client.post("/wallets", headers=headers).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.3,
        }

        response = client.post("/transactions", json=transaction_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["fee_btc"] == 0.0

    def test_transaction_different_user_with_fee(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers1 = {"X-API-KEY": test_user["api_key"]}
        wallet1 = client.post("/wallets", headers=headers1).json()

        user2 = client.post("/users").json()
        headers2 = {"X-API-KEY": user2["api_key"]}
        wallet2 = client.post("/wallets", headers=headers2).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.1,
        }

        response = client.post(
            "/transactions", json=transaction_data, headers=headers1
        )
        assert response.status_code == 201
        data = response.json()
        assert data["fee_btc"] == 0.0015

    def test_transaction_insufficient_balance(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        wallet1 = client.post("/wallets", headers=headers).json()
        wallet2 = client.post("/wallets", headers=headers).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 2.0,
        }

        response = client.post("/transactions", json=transaction_data, headers=headers)
        assert response.status_code == 400
        assert "Insufficient balance" in response.json()["detail"]


class TestTransactionRetrieval:
    def test_get_all_transactions(
        self, client: TestClient, test_user: dict
    ) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        wallet1 = client.post("/wallets", headers=headers).json()
        wallet2 = client.post("/wallets", headers=headers).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.2,
        }
        client.post("/transactions", json=transaction_data, headers=headers)

        response = client.get("/transactions", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["amount_btc"] == 0.2

    def test_get_wallet_transactions(self, client: TestClient, test_user: dict) -> None:
        headers = {"X-API-KEY": test_user["api_key"]}
        wallet1 = client.post("/wallets", headers=headers).json()
        wallet2 = client.post("/wallets", headers=headers).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.15,
        }
        client.post("/transactions", json=transaction_data, headers=headers)

        response = client.get(
            f"/transactions/wallets/{wallet1['address']}/transactions", headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_transactions_requires_api_key(self, client: TestClient) -> None:
        response = client.get("/transactions")
        assert response.status_code == 422

