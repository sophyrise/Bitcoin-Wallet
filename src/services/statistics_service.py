from src.repositories.transaction_repository import TransactionRepository
from src.schemas.statistics import StatisticsResponse


class StatisticsService:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self.transaction_repository = transaction_repository

    async def get_statistics(self) -> StatisticsResponse:
        pass

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100000000

    async def get_btc_to_usd_rate(self) -> float:
        pass

