import pytest
from fastapi.testclient import TestClient


class TestStatistics:
    def test_get_statistics_success(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        response = client.get("/statistics", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_transactions" in data
        assert "platform_profit_btc" in data
        assert "platform_profit_usd" in data

    def test_get_statistics_requires_admin_key(self, client: TestClient) -> None:
        response = client.get("/statistics")
        assert response.status_code == 422

        response = client.get("/statistics", headers={"X-API-KEY": "bad-key"})
        assert response.status_code == 403

    def test_statistics_total_transactions(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        before = client.get("/statistics", headers=admin_headers).json()[
            "total_transactions"
        ]

        user1 = client.post("/users").json()
        user2 = client.post("/users").json()
        headers1 = {"X-API-KEY": user1["api_key"]}
        wallet1 = client.post("/wallets", headers=headers1).json()
        wallet2 = client.post("/wallets", headers={"X-API-KEY": user2["api_key"]}).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.1,
        }
        response = client.post(
            "/transactions", json=transaction_data, headers=headers1
        )
        assert response.status_code == 201

        after = client.get("/statistics", headers=admin_headers).json()[
            "total_transactions"
        ]
        assert after == before + 1

    def test_statistics_platform_profit(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        before_stats = client.get("/statistics", headers=admin_headers).json()
        before_profit_btc = before_stats["platform_profit_btc"]
        before_profit_usd = before_stats["platform_profit_usd"]

        user1 = client.post("/users").json()
        user2 = client.post("/users").json()
        headers1 = {"X-API-KEY": user1["api_key"]}
        wallet1 = client.post("/wallets", headers=headers1).json()
        wallet2 = client.post("/wallets", headers={"X-API-KEY": user2["api_key"]}).json()

        transaction_data = {
            "from_address": wallet1["address"],
            "to_address": wallet2["address"],
            "amount_btc": 0.1,
        }
        response = client.post(
            "/transactions", json=transaction_data, headers=headers1
        )
        assert response.status_code == 201

        after_stats = client.get("/statistics", headers=admin_headers).json()
        expected_fee_btc = 0.0015
        assert after_stats["platform_profit_btc"] == pytest.approx(
            before_profit_btc + expected_fee_btc, rel=1e-6
        )
        assert after_stats["platform_profit_usd"] > before_profit_usd

