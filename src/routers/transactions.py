from typing import List
from fastapi import APIRouter, Depends, Header
from src.schemas.transaction import TransactionCreate, TransactionResponse
from src.services.transaction_service import TransactionService
from src.services.user_service import UserService
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.wallet_repository import WalletRepository
from src.repositories.user_repository import UserRepository
from src.database import database

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_transaction_service() -> TransactionService:
    transaction_repository = TransactionRepository(database)
    wallet_repository = WalletRepository(database)
    return TransactionService(transaction_repository, wallet_repository)


def get_user_service() -> UserService:
    user_repository = UserRepository(database)
    return UserService(user_repository)


async def get_current_user_id(
    x_api_key: str = Header(...),
    user_service: UserService = Depends(get_user_service),
) -> int:
    pass


@router.post("", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate,
    user_id: int = Depends(get_current_user_id),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    pass


@router.get("", response_model=List[TransactionResponse])
async def get_transactions(
    user_id: int = Depends(get_current_user_id),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> List[TransactionResponse]:
    pass


@router.get("/wallets/{address}/transactions", response_model=List[TransactionResponse])
async def get_wallet_transactions(
    address: str,
    user_id: int = Depends(get_current_user_id),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> List[TransactionResponse]:
    pass

