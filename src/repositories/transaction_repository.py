from __future__ import annotations

from src.database import Database
from src.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self, from_address: str, to_address: str, amount: int, fee: int
    ) -> Transaction:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO transactions (from_address, to_address, amount, fee)
                VALUES (?, ?, ?, ?)
                """,
                (from_address, to_address, amount, fee),
            )
            transaction_id = cursor.lastrowid
            cursor.execute(
                "SELECT * FROM transactions WHERE id = ?",
                (transaction_id,),
            )
            row = cursor.fetchone()
            return Transaction.from_row(row)

    def get_by_user(self, user_id: int) -> list[Transaction]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT t.* FROM transactions t
                JOIN wallets w1 ON t.from_address = w1.address
                WHERE w1.user_id = ?
                UNION
                SELECT DISTINCT t.* FROM transactions t
                JOIN wallets w2 ON t.to_address = w2.address
                WHERE w2.user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id, user_id),
            )
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]

    def get_by_wallet(self, address: str) -> list[Transaction]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM transactions
                WHERE from_address = ? OR to_address = ?
                ORDER BY created_at DESC
                """,
                (address, address),
            )
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]

    def get_all(self) -> list[Transaction]:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [Transaction.from_row(row) for row in rows]

    def get_total_fees(self) -> int:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(fee), 0) as total FROM transactions")
            row = cursor.fetchone()
            return int(row["total"])

    def get_total_count(self) -> int:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM transactions")
            row = cursor.fetchone()
            return int(row["count"])

