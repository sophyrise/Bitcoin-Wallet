from pydantic import BaseModel
from datetime import datetime


class WalletCreate(BaseModel):
    pass


class WalletResponse(BaseModel):
    address: str
    balance_btc: float
    balance_usd: float


class WalletInDB(BaseModel):
    id: int
    address: str
    user_id: int
    balance: int
    created_at: datetime

    class Config:
        from_attributes = True

