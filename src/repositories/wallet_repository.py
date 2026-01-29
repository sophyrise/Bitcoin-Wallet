from typing import Optional, List
from src.database import Database
from src.models.wallet import Wallet


class WalletRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, address: str, user_id: int, initial_balance: int) -> Wallet:
        pass

    def get_by_address(self, address: str) -> Optional[Wallet]:
        pass

    def get_by_user_id(self, user_id: int) -> List[Wallet]:
        pass

    def count_by_user_id(self, user_id: int) -> int:
        pass

    def update_balance(self, wallet_id: int, new_balance: int) -> None:
        pass

