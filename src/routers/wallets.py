from fastapi import APIRouter, Depends

from src.database import database
from src.middleware.auth import verify_api_key
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.wallet import WalletResponse
from src.services.wallet_service import WalletService

router = APIRouter(prefix="/wallets", tags=["Wallets"])


def get_wallet_service() -> WalletService:
    wallet_repository = WalletRepository(database)
    user_repository = UserRepository(database)
    return WalletService(wallet_repository, user_repository)


@router.post("", response_model=WalletResponse, status_code=201)
async def create_wallet(
    user_id: int = Depends(verify_api_key),
    wallet_service: WalletService = Depends(get_wallet_service),
) -> WalletResponse:
    return await wallet_service.create_wallet(user_id)


@router.get("/{address}", response_model=WalletResponse)
async def get_wallet(
    address: str,
    user_id: int = Depends(verify_api_key),
    wallet_service: WalletService = Depends(get_wallet_service),
) -> WalletResponse:
    return await wallet_service.get_wallet(address, user_id)

