from pydantic import BaseModel


class AdminUserWalletsResponse(BaseModel):
    user_id: int
    api_key: str
    wallets: list[str]
