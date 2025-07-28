from typing import Optional
import sqlite3
from contextlib import contextmanager
import os
import os.path

from medai_flow.database.base_database import BaseDatabase
from medai_flow.utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class SqliteDatabase(BaseDatabase):
    """Base database class providing SQLite connection handling."""

    def __init__(self, path: str = "longevity_qa.db"):
        """Initialize database with configuration."""
        self.path = os.path.abspath(path)
        self._ensure_db_dir()

    def _ensure_db_dir(self) -> None:
        db_dir = os.path.dirname(self.path)
        os.makedirs(db_dir, exist_ok=True)
        if not os.access(db_dir, os.W_OK):
            logger.error(f"No write permission for directory: {db_dir}")
            raise PermissionError(f"No write permission for directory: {db_dir}")
        logger.info(f"Using database path: {self.path}")
        try:
            conn = sqlite3.connect(self.path)
            conn.close()
            logger.info(f"Successfully connected to database at {self.path}")
        except sqlite3.OperationalError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise sqlite3.OperationalError(
                f"Unable to open database at {self.path}. "
                f"Try using an absolute path or check directory permissions."
            ) from e

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.path)
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> None:
        with self.get_connection() as conn:
            conn.execute(query, params)
            conn.commit()

    def query_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()

    def query_all(self, query: str, params: tuple = ()) -> list[tuple]:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
