from __future__ import annotations

from src.database import Database
from src.models.wallet import Wallet


class WalletRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, address: str, user_id: int, initial_balance: int) -> Wallet:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO wallets (address, user_id, balance, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                (address, user_id, initial_balance),
            )
            wallet_id = cursor.lastrowid
            cursor.execute(
                "SELECT * FROM wallets WHERE id = ?",
                (wallet_id,),
            )
            row = cursor.fetchone()
            return Wallet.from_row(row)

    def get_by_address(self, address: str) -> Wallet | None:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM wallets WHERE address = ?",
                (address,),
            )
            row = cursor.fetchone()
            return Wallet.from_row(row) if row else None

    def get_by_user_id(self, user_id: int) -> list[Wallet]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM wallets WHERE user_id = ?",
                (user_id,),
            )
            rows = cursor.fetchall()
            return [Wallet.from_row(row) for row in rows]

    def count_by_user_id(self, user_id: int) -> int:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) as count FROM wallets WHERE user_id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            return int(row["count"])

    def update_balance(self, wallet_id: int, new_balance: int) -> None:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE wallets SET balance = ? WHERE id = ?",
                (new_balance, wallet_id),
            )

    def get_addresses_by_user_ids(
        self, user_ids: list[int]
    ) -> dict[int, list[str]]:
        if not user_ids:
            return {}

        placeholders = ", ".join(["?"] * len(user_ids))
        query = (
            "SELECT user_id, address FROM wallets "
            f"WHERE user_id IN ({placeholders}) "
            "ORDER BY user_id ASC, created_at ASC"
        )

        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(user_ids))
            rows = cursor.fetchall()

        addresses: dict[int, list[str]] = {}
        for row in rows:
            user_id = int(row["user_id"])
            addresses.setdefault(user_id, []).append(row["address"])
        return addresses

