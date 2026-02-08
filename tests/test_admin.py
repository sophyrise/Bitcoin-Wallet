from fastapi.testclient import TestClient


class TestAdminUsersWallets:
    def test_admin_users_wallets_requires_admin_key(
        self, client: TestClient
    ) -> None:
        response = client.get("/admin/users-wallets")
        assert response.status_code == 422

        response = client.get(
            "/admin/users-wallets", headers={"X-API-KEY": "bad-key"}
        )
        assert response.status_code == 403

    def test_admin_users_wallets_returns_users_and_wallets(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        user1 = client.post("/users").json()
        user2 = client.post("/users").json()

        headers1 = {"X-API-KEY": user1["api_key"]}
        headers2 = {"X-API-KEY": user2["api_key"]}

        wallet1 = client.post("/wallets", headers=headers1).json()
        wallet2 = client.post("/wallets", headers=headers1).json()
        wallet3 = client.post("/wallets", headers=headers2).json()

        response = client.get("/admin/users-wallets", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) >= 2

        by_api_key = {item["api_key"]: item for item in data}
        assert user1["api_key"] in by_api_key
        assert user2["api_key"] in by_api_key

        assert wallet1["address"] in by_api_key[user1["api_key"]]["wallets"]
        assert wallet2["address"] in by_api_key[user1["api_key"]]["wallets"]
        assert wallet3["address"] in by_api_key[user2["api_key"]]["wallets"]


class TestAdminReports:
    def test_admin_total_balances(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        response = client.get("/admin/reports/total-balances", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_balance_btc" in data
        assert "total_balance_usd" in data
        assert data["total_balance_btc"] >= 0
        assert data["total_balance_usd"] >= 0

    def test_admin_top_users(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        response = client.get(
            "/admin/reports/top-users?limit=3", headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 3
        if data:
            sample = data[0]
            assert "user_id" in sample
            assert "api_key" in sample
            assert "wallet_count" in sample
            assert "total_balance_btc" in sample
            assert "total_balance_usd" in sample

    def test_admin_fees_by_day(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        user1 = client.post("/users").json()
        user2 = client.post("/users").json()
        headers1 = {"X-API-KEY": user1["api_key"]}
        headers2 = {"X-API-KEY": user2["api_key"]}

        wallet1 = client.post("/wallets", headers=headers1).json()
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

        response = client.get(
            "/admin/reports/fees-by-day", headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            sample = data[0]
            assert "day" in sample
            assert "total_fee_btc" in sample
            assert "total_fee_usd" in sample
