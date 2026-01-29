from __future__ import annotations

from src.database import Database
from src.models.user import User


class UserRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, api_key: str) -> User:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (api_key) VALUES (?)",
                (api_key,),
            )
            user_id = cursor.lastrowid
            cursor.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            return User.from_row(row)

    def get_by_api_key(self, api_key: str) -> User | None:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE api_key = ?",
                (api_key,),
            )
            row = cursor.fetchone()
            return User.from_row(row) if row else None

    def get_by_id(self, user_id: int) -> User | None:
        with self.database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            return User.from_row(row) if row else None

