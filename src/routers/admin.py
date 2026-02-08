from fastapi import APIRouter, Depends, Query

from src.database import database
from src.middleware.auth import verify_admin_key
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.admin import (
    AdminFeeByDayResponse,
    AdminTopUserResponse,
    AdminTotalBalancesResponse,
    AdminUserWalletsResponse,
)
from src.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


def get_admin_service() -> AdminService:
    user_repository = UserRepository(database)
    wallet_repository = WalletRepository(database)
    transaction_repository = TransactionRepository(database)
    return AdminService(user_repository, wallet_repository, transaction_repository)


@router.get("/users-wallets", response_model=list[AdminUserWalletsResponse])
async def get_users_wallets(
    admin_verified: None = Depends(verify_admin_key),
    admin_service: AdminService = Depends(get_admin_service),
) -> list[AdminUserWalletsResponse]:
    return admin_service.get_users_wallets()


@router.get("/reports/total-balances", response_model=AdminTotalBalancesResponse)
async def get_total_balances(
    admin_verified: None = Depends(verify_admin_key),
    admin_service: AdminService = Depends(get_admin_service),
) -> AdminTotalBalancesResponse:
    return await admin_service.get_total_balances()


@router.get("/reports/top-users", response_model=list[AdminTopUserResponse])
async def get_top_users(
    limit: int = Query(5, ge=1, le=100),
    admin_verified: None = Depends(verify_admin_key),
    admin_service: AdminService = Depends(get_admin_service),
) -> list[AdminTopUserResponse]:
    return await admin_service.get_top_users(limit)


@router.get("/reports/fees-by-day", response_model=list[AdminFeeByDayResponse])
async def get_fees_by_day(
    limit: int | None = Query(None, ge=1, le=365),
    admin_verified: None = Depends(verify_admin_key),
    admin_service: AdminService = Depends(get_admin_service),
) -> list[AdminFeeByDayResponse]:
    return await admin_service.get_fee_breakdown_by_day(limit)
