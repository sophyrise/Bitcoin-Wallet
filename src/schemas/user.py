from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    pass


class UserResponse(BaseModel):
    api_key: str


class UserInDB(BaseModel):
    id: int
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True

