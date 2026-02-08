from pydantic import BaseModel


class AdminUserWalletsResponse(BaseModel):
    user_id: int
    api_key: str
    wallets: list[str]


class AdminTotalBalancesResponse(BaseModel):
    total_balance_btc: float
    total_balance_usd: float


class AdminTopUserResponse(BaseModel):
    user_id: int
    api_key: str
    wallet_count: int
    total_balance_btc: float
    total_balance_usd: float


class AdminFeeByDayResponse(BaseModel):
    day: str
    total_fee_btc: float
    total_fee_usd: float
