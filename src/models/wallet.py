from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Wallet:
    id: int
    address: str
    user_id: int
    balance: int
    created_at: datetime
    
    @classmethod
    def from_row(cls, row) -> "Wallet":
        return cls(
            id=row["id"],
            address=row["address"],
            user_id=row["user_id"],
            balance=row["balance"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

