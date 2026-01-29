from fastapi import Header, HTTPException, status
from src.services.user_service import UserService


async def verify_api_key(
    x_api_key: str = Header(...), user_service: UserService = None
) -> int:
    pass


async def verify_admin_key(x_api_key: str = Header(...)) -> None:
    pass

