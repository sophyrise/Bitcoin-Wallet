from fastapi import APIRouter, Depends

from src.database import database
from src.middleware.auth import verify_admin_key
from src.repositories.transaction_repository import TransactionRepository
from src.schemas.statistics import StatisticsResponse
from src.services.statistics_service import StatisticsService

router = APIRouter(prefix="/statistics", tags=["Statistics"])


def get_statistics_service() -> StatisticsService:
    transaction_repository = TransactionRepository(database)
    return StatisticsService(transaction_repository)

@router.get("", response_model=StatisticsResponse)
async def get_statistics(
    admin_verified: None = Depends(verify_admin_key),
    statistics_service: StatisticsService = Depends(get_statistics_service),
) -> StatisticsResponse:
    return await statistics_service.get_statistics()

