from fastapi import APIRouter, Depends, Header

from src.database import database
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.wallet import WalletResponse
from src.services.user_service import UserService
from src.services.wallet_service import WalletService

router = APIRouter(prefix="/wallets", tags=["Wallets"])


def get_wallet_service() -> WalletService:
    wallet_repository = WalletRepository(database)
    user_repository = UserRepository(database)
    return WalletService(wallet_repository, user_repository)


def get_user_service() -> UserService:
    user_repository = UserRepository(database)
    return UserService(user_repository)


async def get_current_user_id(
    x_api_key: str = Header(...),
    user_service: UserService = Depends(get_user_service),
) -> int:
    pass


@router.post("", response_model=WalletResponse, status_code=201)
async def create_wallet(
    user_id: int = Depends(get_current_user_id),
    wallet_service: WalletService = Depends(get_wallet_service),
) -> WalletResponse:
    pass


@router.get("/{address}", response_model=WalletResponse)
async def get_wallet(
    address: str,
    user_id: int = Depends(get_current_user_id),
    wallet_service: WalletService = Depends(get_wallet_service),
) -> WalletResponse:
    pass

