from fastapi.testclient import TestClient


class TestStatistics:
    def test_get_statistics_success(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        pass

    def test_get_statistics_requires_admin_key(self, client: TestClient) -> None:
        pass

    def test_statistics_total_transactions(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        pass

    def test_statistics_platform_profit(
        self, client: TestClient, admin_headers: dict
    ) -> None:
        pass

