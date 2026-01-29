from __future__ import annotations

import sqlite3
from contextlib import contextmanager

from src.config import settings


class Database:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or settings.database_path
        self._init_database()

    def _init_database(self) -> None:
        self.create_tables()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_tables(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    api_key TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS wallets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    balance INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_address TEXT NOT NULL,
                    to_address TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    fee INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_address) REFERENCES wallets (address),
                    FOREIGN KEY (to_address) REFERENCES wallets (address)
                )
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_wallets_user_id 
                ON wallets(user_id)
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_wallets_address 
                ON wallets(address)
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_transactions_from_address 
                ON transactions(from_address)
                """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_transactions_to_address 
                ON transactions(to_address)
                """
            )

            conn.commit()


database = Database()

