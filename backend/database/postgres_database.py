from typing import Optional, Any
import psycopg2
from contextlib import contextmanager

from database.base_database import BaseDatabase
from utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class PostgresDatabase(BaseDatabase):
    """Postgres database class providing PostgresQL connection handling."""

    def __init__(self, dbname: str, user: str, password:str, host: str="localhost", port: int=5432):
        """Initialize database with configuration.

        Args:
            config: Database configuration containing connection details
        """
        self.config = dict(dbname=dbname, user=user, password=password, host=host, port=port)
        try:
            # Test connection
            conn = psycopg2.connect(**self.config)
            conn.close()
            logger.info(f"Successfully connected to database {dbname}@{host}")
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Failed to connect to database {dbname}@{host}: {e}")

    def _format_query(self, query: str):
        # Replace all placeholders with appropriate style
        _query = query.replace("?", "%s")
        _query = _query.replace("BLOB", "BYTEA")
        _query = _query.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        return _query

    @contextmanager
    def get_connection(self):
        """Get database connection as context manager.

        Yields:
            Connection: Database connection
        """
        conn = psycopg2.connect(**self.config)
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a query without returning results.

        Args:
            query: SQL query to execute
            params: Query parameters
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(self._format_query(query), params)
            conn.commit()
            logger.info(f"{cur.query}: {cur.statusmessage}")

    def execute_return(self, query: str, params: tuple = ()) -> Any:
        """Execute a query and return the result directly.

        This method is useful for INSERT ... RETURNING, UPDATE ... RETURNING, etc.
        where you want to get the returned value in a single operation.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            Any: The result of the query execution
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(self._format_query(query), params)
            result = cur.fetchone()
            conn.commit()
            logger.info(f"{cur.query}: {cur.statusmessage}")
            return result[0] if result else None

    async def query_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """Execute a query and return one result.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            Optional[tuple]: Query result or None if no results
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            logger.info(f"{cur.query}: {cur.statusmessage}")
            result = cur.fetchone()
            conn.commit()
            return result

    def query_all(self, query: str, params: tuple = ()) -> list[tuple]:
        """Execute a query and return all results.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            list[tuple]: List of query results
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(self._format_query(query), params)
            logger.info(f"{cur.query}: {cur.statusmessage}")
            result = cur.fetchall()
            conn.commit()
            return result
