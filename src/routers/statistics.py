from fastapi import APIRouter, Depends, Header

from src.database import database
from src.repositories.transaction_repository import TransactionRepository
from src.schemas.statistics import StatisticsResponse
from src.services.statistics_service import StatisticsService

router = APIRouter(prefix="/statistics", tags=["Statistics"])


def get_statistics_service() -> StatisticsService:
    transaction_repository = TransactionRepository(database)
    return StatisticsService(transaction_repository)


async def verify_admin_key(x_api_key: str = Header(...)) -> None:
    pass


@router.get("", response_model=StatisticsResponse)
async def get_statistics(
    admin_verified: None = Depends(verify_admin_key),
    statistics_service: StatisticsService = Depends(get_statistics_service),
) -> StatisticsResponse:
    pass

