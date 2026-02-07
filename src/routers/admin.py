from fastapi import APIRouter, Depends

from src.database import database
from src.middleware.auth import verify_admin_key
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.admin import AdminUserWalletsResponse
from src.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_admin_service() -> AdminService:
    user_repository = UserRepository(database)
    wallet_repository = WalletRepository(database)
    return AdminService(user_repository, wallet_repository)


@router.get("/users-wallets", response_model=list[AdminUserWalletsResponse])
async def get_users_wallets(
    admin_verified: None = Depends(verify_admin_key),
    admin_service: AdminService = Depends(get_admin_service),
) -> list[AdminUserWalletsResponse]:
    return admin_service.get_users_wallets()
