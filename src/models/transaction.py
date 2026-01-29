from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    id: int
    from_address: str
    to_address: str
    amount: int
    fee: int
    created_at: datetime
    
    @classmethod
    def from_row(cls, row) -> "Transaction":
        return cls(
            id=row["id"],
            from_address=row["from_address"],
            to_address=row["to_address"],
            amount=row["amount"],
            fee=row["fee"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

