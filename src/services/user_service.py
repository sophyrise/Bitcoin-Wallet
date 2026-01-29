from src.repositories.user_repository import UserRepository
from src.schemas.user import UserResponse


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(self) -> UserResponse:
        pass

    def authenticate(self, api_key: str) -> bool:
        pass

    def get_user_id_by_api_key(self, api_key: str) -> int:
        pass

