
from __future__ import annotations

from src.repositories.transaction_repository import TransactionRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.transaction import TransactionCreate, TransactionResponse


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        wallet_repository: WalletRepository,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.wallet_repository = wallet_repository

    def create_transaction(
        self, transaction_data: TransactionCreate, user_id: int
    ) -> TransactionResponse:
        pass

    def get_transactions_by_user(self, user_id: int) -> list[TransactionResponse]:
        pass

    def get_transactions_by_wallet(
        self, address: str, user_id: int
    ) -> list[TransactionResponse]:
        pass

    def calculate_fee(self, amount: int, is_same_user: bool) -> int:
        pass

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100000000

