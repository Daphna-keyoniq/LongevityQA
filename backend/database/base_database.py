from abc import ABC, abstractmethod
from typing import Optional
from contextlib import contextmanager

class BaseDatabase(ABC):
    """Base database"""

    @contextmanager
    @abstractmethod
    def get_connection(self):
        """Get database connection as context manager.

        Yields:
            Connection: Database connection
        """
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple = ()) -> None:
        """Execute a query without returning results,
           use context manager 'with' clause.

        Args:
            query: SQL query to execute
            params: Query parameters
        """
        pass

    @abstractmethod
    def query_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """Execute a query and return one result,
           use context manager 'with' clause.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            Optional[tuple]: Query result or None if no results
        """
        pass

    @abstractmethod
    def query_all(self, query: str, params: tuple = ()) -> list[tuple]:
        """Execute a query and return all results,
           use context manager 'with' clause.

        Args:
            query: SQL query to execute
            params: Query parameters

        Returns:
            list[tuple]: List of query results
        """
        pass

