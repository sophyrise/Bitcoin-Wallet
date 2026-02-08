from __future__ import annotations

import secrets

import httpx
from fastapi import HTTPException, status

from src.config import settings
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.wallet import WalletResponse


class WalletService:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        user_repository: UserRepository,
    ) -> None:
        self.wallet_repository = wallet_repository
        self.user_repository = user_repository

    async def create_wallet(self, user_id: int) -> WalletResponse:
        wallet_count = self.wallet_repository.count_by_user_id(user_id)
        if wallet_count >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum wallet limit reached (3 wallets per user)",
            )

        address = self._generate_wallet_address()
        initial_balance = 100_000_000
        wallet = self.wallet_repository.create(address, user_id, initial_balance)

        btc_usd_rate = await self.get_btc_to_usd_rate()
        balance_btc = self.satoshi_to_btc(wallet.balance)
        balance_usd = balance_btc * btc_usd_rate

        return WalletResponse(
            address=wallet.address,
            balance_btc=balance_btc,
            balance_usd=balance_usd,
        )

    async def get_wallet(self, address: str, user_id: int) -> WalletResponse:
        wallet = self.wallet_repository.get_by_address(address)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found",
            )

        if wallet.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this wallet",
            )

        btc_usd_rate = await self.get_btc_to_usd_rate()
        balance_btc = self.satoshi_to_btc(wallet.balance)
        balance_usd = balance_btc * btc_usd_rate

        return WalletResponse(
            address=wallet.address,
            balance_btc=balance_btc,
            balance_usd=balance_usd,
        )

    async def get_wallets_by_user(self, user_id: int) -> list[WalletResponse]:
        wallets = self.wallet_repository.get_by_user_id(user_id)
        btc_usd_rate = await self.get_btc_to_usd_rate()

        wallet_responses = []
        for wallet in wallets:
            balance_btc = self.satoshi_to_btc(wallet.balance)
            balance_usd = balance_btc * btc_usd_rate
            wallet_responses.append(
                WalletResponse(
                    address=wallet.address,
                    balance_btc=balance_btc,
                    balance_usd=balance_usd,
                )
            )

        return wallet_responses

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100_000_000

    def btc_to_satoshi(self, btc: float) -> int:
        return int(btc * 100_000_000)

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

    def _generate_wallet_address(self) -> str:
        return secrets.token_hex(20)

