from fastapi import APIRouter, Depends
from src.schemas.user import UserResponse
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.database import database

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service() -> UserService:
    user_repository = UserRepository(database)
    return UserService(user_repository)


@router.post("", response_model=UserResponse, status_code=201)
async def register_user(
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    pass

