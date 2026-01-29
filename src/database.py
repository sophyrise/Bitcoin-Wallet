import sqlite3
from contextlib import contextmanager

from src.config import settings


class Database:
    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or settings.database_path
        self._init_database()

    def _init_database(self) -> None:
        pass

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_tables(self) -> None:
        pass


database = Database()

