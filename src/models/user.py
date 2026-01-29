from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    api_key: str
    created_at: datetime
    
    @classmethod
    def from_row(cls, row) -> "User":
        return cls(
            id=row["id"],
            api_key=row["api_key"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

