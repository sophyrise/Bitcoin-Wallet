import httpx

from src.config import settings
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.admin import (
    AdminFeeByDayResponse,
    AdminTopUserResponse,
    AdminTotalBalancesResponse,
    AdminUserWalletsResponse,
)


class AdminService:
    def __init__(
        self,
        user_repository: UserRepository,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
    ) -> None:
        self.user_repository = user_repository
        self.wallet_repository = wallet_repository
        self.transaction_repository = transaction_repository

    def get_users_wallets(self) -> list[AdminUserWalletsResponse]:
        users = self.user_repository.get_all()
        if not users:
            return []

        addresses_by_user = self.wallet_repository.get_addresses_by_user_ids(
            [user.id for user in users]
        )

        return [
            AdminUserWalletsResponse(
                user_id=user.id,
                api_key=user.api_key,
                wallets=addresses_by_user.get(user.id, []),
            )
            for user in users
        ]

    async def get_total_balances(self) -> AdminTotalBalancesResponse:
        total_balance_satoshi = self.wallet_repository.get_total_balance()
        total_balance_btc = self.satoshi_to_btc(total_balance_satoshi)
        btc_usd_rate = await self.get_btc_to_usd_rate()
        total_balance_usd = total_balance_btc * btc_usd_rate
        return AdminTotalBalancesResponse(
            total_balance_btc=total_balance_btc,
            total_balance_usd=total_balance_usd,
        )

    async def get_top_users(self, limit: int) -> list[AdminTopUserResponse]:
        top_users = self.wallet_repository.get_top_users_by_balance(limit)
        if not top_users:
            return []

        btc_usd_rate = await self.get_btc_to_usd_rate()
        return [
            AdminTopUserResponse(
                user_id=item["user_id"],
                api_key=item["api_key"],
                wallet_count=item["wallet_count"],
                total_balance_btc=self.satoshi_to_btc(item["total_balance"]),
                total_balance_usd=self.satoshi_to_btc(item["total_balance"])
                * btc_usd_rate,
            )
            for item in top_users
        ]

    async def get_fee_breakdown_by_day(
        self, limit: int | None
    ) -> list[AdminFeeByDayResponse]:
        fee_by_day = self.transaction_repository.get_fee_breakdown_by_day(limit)
        if not fee_by_day:
            return []

        btc_usd_rate = await self.get_btc_to_usd_rate()
        return [
            AdminFeeByDayResponse(
                day=item["day"],
                total_fee_btc=self.satoshi_to_btc(item["total_fee"]),
                total_fee_usd=self.satoshi_to_btc(item["total_fee"]) * btc_usd_rate,
            )
            for item in fee_by_day
        ]

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100_000_000

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
