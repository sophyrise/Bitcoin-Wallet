from datetime import datetime

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    from_address: str
    to_address: str
    amount_btc: float


class TransactionResponse(BaseModel):
    id: int
    from_address: str
    to_address: str
    amount_btc: float
    fee_btc: float
    created_at: datetime


class TransactionInDB(BaseModel):
    id: int
    from_address: str
    to_address: str
    amount: int
    fee: int
    created_at: datetime

    class Config:
        from_attributes = True

