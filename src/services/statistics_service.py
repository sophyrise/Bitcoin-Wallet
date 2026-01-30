import httpx

from src.config import settings
from src.repositories.transaction_repository import TransactionRepository
from src.schemas.statistics import StatisticsResponse


class StatisticsService:
    def __init__(self, transaction_repository: TransactionRepository) -> None:
        self.transaction_repository = transaction_repository

    async def get_statistics(self) -> StatisticsResponse:
        total_transactions = self.transaction_repository.get_total_count()
        total_fees_satoshi = self.transaction_repository.get_total_fees()
        platform_profit_btc = self.satoshi_to_btc(total_fees_satoshi)
        btc_usd_rate = await self.get_btc_to_usd_rate()
        platform_profit_usd = platform_profit_btc * btc_usd_rate

        return StatisticsResponse(
            total_transactions=total_transactions,
            platform_profit_btc=platform_profit_btc,
            platform_profit_usd=platform_profit_usd,
        )

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100000000

    async def get_btc_to_usd_rate(self) -> float:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(settings.btc_usd_api_url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                usd_rate = float(data["data"]["rates"]["USD"])
                return usd_rate
        except Exception:
            return 45000.0

