from pydantic import BaseModel


class StatisticsResponse(BaseModel):
    total_transactions: int
    platform_profit_btc: float
    platform_profit_usd: float

