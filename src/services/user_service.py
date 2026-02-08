import secrets

from fastapi import HTTPException, status

from src.repositories.user_repository import UserRepository
from src.schemas.user import UserResponse


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(self) -> UserResponse:
        api_key = self._generate_api_key()
        user = self.user_repository.create(api_key)
        return UserResponse(api_key=user.api_key)

    def authenticate(self, api_key: str) -> bool:
        user = self.user_repository.get_by_api_key(api_key)
        return user is not None

    def get_user_id_by_api_key(self, api_key: str) -> int:
        user = self.user_repository.get_by_api_key(api_key)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )
        return user.id

    def _generate_api_key(self) -> str:
        return secrets.token_urlsafe(32)

