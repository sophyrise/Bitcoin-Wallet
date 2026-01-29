
from src.database import Database
from src.models.user import User


class UserRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, api_key: str) -> User:
        pass

    def get_by_api_key(self, api_key: str) -> User | None:
        pass

    def get_by_id(self, user_id: int) -> User | None:
        pass

