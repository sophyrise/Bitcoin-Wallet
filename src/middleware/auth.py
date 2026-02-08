from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status

from src.config import settings
from src.database import database
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService


def get_user_service() -> UserService:
    user_repository = UserRepository(database)
    return UserService(user_repository)


async def verify_api_key(
    x_api_key: str = Header(...),
    user_service: UserService = Depends(get_user_service),
) -> int:
    user_id = user_service.get_user_id_by_api_key(x_api_key)
    return user_id


async def verify_admin_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key",
        )

