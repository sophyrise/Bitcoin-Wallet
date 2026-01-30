from __future__ import annotations

from fastapi import APIRouter, Depends

from src.database import database
from src.middleware.auth import verify_api_key
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.transaction import TransactionCreate, TransactionResponse
from src.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_transaction_service() -> TransactionService:
    transaction_repository = TransactionRepository(database)
    wallet_repository = WalletRepository(database)
    return TransactionService(transaction_repository, wallet_repository)


@router.post("", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction_data: TransactionCreate,
    user_id: int = Depends(verify_api_key),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    return transaction_service.create_transaction(transaction_data, user_id)


@router.get("", response_model=list[TransactionResponse])
async def get_transactions(
    user_id: int = Depends(verify_api_key),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> list[TransactionResponse]:
    return transaction_service.get_transactions_by_user(user_id)


@router.get("/wallets/{address}/transactions", response_model=list[TransactionResponse])
async def get_wallet_transactions(
    address: str,
    user_id: int = Depends(verify_api_key),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> list[TransactionResponse]:
    return transaction_service.get_transactions_by_wallet(address, user_id)

