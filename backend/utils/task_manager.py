from datetime import datetime
from typing import Optional
import json
# import bcrypt
import os
# from uuid import UUID, uuid4
from pydantic import BaseModel
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from dotenv import load_dotenv

load_dotenv()

## Internal imports
from database import BaseDatabase
from utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

class TaskStatus(BaseModel):
    """Model for task status information."""

    task_id: int
    task_input: str
    status: str
    message: str
    record_entered_timestamp: datetime
    result: Optional[dict] = None

class Rating(BaseModel):
    task_id: int
    rating: str

class User(BaseModel):
    """Base model for user information."""

    user_id: int
    username: str
    email: str
    created_at: datetime
    is_superuser: bool


class TaskManagerRepository:
    """Repository for handling task operations with api."""

    def __init__(self, database: BaseDatabase, schema_name: Optional[str] = None):
        """Initialize repository with database connection.

        Args:
            database: Database instance for data access
            schema_name: Optional schema name for test isolation
        """
        self.database = database
        self.schema_name = schema_name
        self._init_table()
        # self._ensure_default_user(database, is_superuser=True)

    def _init_table(self) -> None:
        """Initialize tasks table if it doesn't exist."""
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""

        self.database.execute(f"""
            CREATE TABLE IF NOT EXISTS {schema_prefix}tasks (
                task_id SERIAL PRIMARY KEY,
                created_at TIMESTAMP NOT NULL
            )
        """)

        # Create task status table for tracking task state
        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {schema_prefix}task_status (
                task_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                message TEXT NOT NULL,
                record_entered_timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY(task_id) REFERENCES {schema_prefix}tasks(task_id)
            )
        """
        )

        # Create separate table for task data and results
        self.database.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {schema_prefix}task_data (
            task_id INTEGER NOT NULL,
            input_data TEXT,
            output_data TEXT,
            PRIMARY KEY (task_id),
            FOREIGN KEY(task_id) REFERENCES {schema_prefix}tasks(task_id)
            )
        """
        )

        # Add is_superuser column if it doesn't exist (for backward compatibility)
        try:
            self.database.execute(f"""
                ALTER TABLE {schema_prefix}users ADD COLUMN IF NOT EXISTS is_superuser BOOLEAN DEFAULT FALSE
            """)
        except Exception as e:
            logger.warning(f"Error adding is_superuser column: {e}")

    def create_task(self) -> int:
        """Create a new task and return its ID.

        Returns:
            int: The ID of the newly created task
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        task_id = self.database.query_one(f"""
            INSERT INTO {schema_prefix}tasks (created_at)
            VALUES (CURRENT_TIMESTAMP)
            RETURNING task_id
        """)
        return task_id[0]

    def save_task(
        self,
        task_status: TaskStatus,
        input_data: Optional[bytes] = None,
        output_data: Optional[bytes] = None,
    ) -> None:
        """Save task status to database.

        Args:
            task_status: Task status to save
            input_data: Optional input data
            output_data: Optional output data
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""

        current_status = self.get_task_status_history(task_status.task_id)
        if any(status.status == "completed" for status in current_status):
            return

        # Save task status
        self.database.execute(
            f"""
            INSERT INTO {schema_prefix}task_status
            (task_id, status, message, record_entered_timestamp)
            VALUES (%s, %s, %s, %s)
        """,
            (
                task_status.task_id,
                task_status.status,
                task_status.message,
                task_status.record_entered_timestamp.isoformat(),
            ),
        )

        # Save task data if provided
        if input_data is not None or output_data is not None:
            # Convert output_data to bytes if it's not already
            if output_data is not None and not isinstance(output_data, bytes):
                output_data = json.dumps(output_data).encode("utf-8")  # type: ignore[unreachable]

            self.database.execute(
                f"""
                INSERT INTO {schema_prefix}task_data (task_id, input_data, output_data)
                VALUES (%s, %s, %s)
                ON CONFLICT (task_id) DO UPDATE
                SET input_data = EXCLUDED.input_data,
                    output_data = EXCLUDED.output_data
                """,
                (task_status.task_id, input_data, output_data),
            )

    def get_task_status_history(self, task_id: int) -> list[TaskStatus]:
        """Retrieve task status history from database.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Optional[TaskStatus]: Task status if found, None otherwise
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        rows = self.database.query_all(
            f"""
            SELECT task_id, status, message, record_entered_timestamp
            FROM {schema_prefix}task_status
            WHERE task_id = %s
            ORDER BY record_entered_timestamp DESC
            """,
            (task_id,),
        )

        if rows:
            return [
                TaskStatus(
                    task_id=row[0],
                    status=row[1],
                    message=row[2],
                    record_entered_timestamp=row[3],
                )
                for row in rows
            ]
        return []

    def get_task_status(self, task_id: int) -> Optional[TaskStatus]:
        """Retrieve task status from database.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Optional[TaskStatus]: Task status if found, None otherwise
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        row = self.database.query_one(
            f"""
            SELECT task_id, status, message, record_entered_timestamp
            FROM {schema_prefix}task_status
            WHERE task_id = %s
            ORDER BY record_entered_timestamp DESC
            LIMIT 1
            """,
            (task_id,),
        )

        if row:
            return TaskStatus(
                task_id=row[0],
                status=row[1],
                message=row[2],
                record_entered_timestamp=row[3],
            )
        return None

    def get_task_output(self, task_id: int) -> Optional[dict]:
        """Get output data for a completed task.

        Args:
            task_id: ID of task to retrieve output for

        Returns:
            Optional[dict]: Output data if found and task completed, None otherwise
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        row = self.database.query_one(
            f"""
            SELECT td.output_data
            FROM {schema_prefix}task_data td
            JOIN {schema_prefix}task_status ts ON td.task_id = ts.task_id
            WHERE td.task_id = %s AND ts.status = %s
            """,
            (task_id, "completed"),
        )
        if row and row[0]:
            # Convert memoryview to bytes before decoding
            return json.loads(bytes(row[0]).decode())
        return None

    def get_all_tasks_ids(self) -> list[int]:
        """Get all task IDs from database.

        Returns:
            list[int]: List of all task IDs
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        results = self.database.query_all(f"SELECT task_id FROM {schema_prefix}tasks")

        return [row[0] for row in results] if results else []


    def get_tasks_status(self, task_id: int) -> list[TaskStatus]:
        """
        Get tasks from database.

        Args:
            task_ids: List of task IDs to get

        Returns:
            List of TaskStatus objects
        """
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        rows = self.database.query_all(
            f"""
            SELECT ts.task_id, ts.status, ts.message, td.output_data, ts.record_entered_timestamp
            FROM {schema_prefix}task_status ts
            LEFT JOIN {schema_prefix}task_data td ON ts.task_id = td.task_id
            WHERE ts.task_id = %s
            """,
            (task_id,),
        )
        return [
            TaskStatus(
                task_id=row[0],
                status=row[1],
                message=row[2],
                result=json.loads(row[3].decode()) if row[3] else None,
                record_entered_timestamp=row[4],
            )
            for row in rows
        ]

    def _ensure_default_user(
        self,
        database: BaseDatabase,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        is_superuser: bool = True,
    ):
        """Creates a default dev user if it doesn't exist yet.

        Args:
            database: Database instance to use
            username: Username for default user. If None, reads from DEV_USERNAME env var
            email: Email for default user. If None, reads from DEV_EMAIL env var
            password: Password for default user. If None, reads from DEV_PASSWORD env var
            is_superuser: Whether the default user should be a superuser (default: True)
        """
        # Use provided credentials or fall back to environment variables
        username = username or os.getenv("DEV_USERNAME")
        email = email or os.getenv("DEV_EMAIL")
        password = password or os.getenv("DEV_PASSWORD")

        if not username or not email or not password:
            logger.warning("Default dev user credentials are missing")
            return

        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        exists = database.query_one(
            f"SELECT 1 FROM {schema_prefix}users WHERE username = %s OR email = %s",
            (username, email),
        )
        if exists:
            # Update existing default user to be a superuser if not already
            try:
                database.execute(
                    f"UPDATE {schema_prefix}users SET is_superuser = TRUE WHERE username = %s AND is_superuser = FALSE",
                    (username,),
                )
                logger.info(f"Updated default user '{username}' to superuser.")
            except Exception as e:
                logger.warning(f"Error updating default user to superuser: {e}")
            return

        password_hash = self._hash_pw(password)
        with database.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO {schema_prefix}users (username, email, password_hash, created_at, is_superuser) VALUES (%s, %s, %s, %s, %s)",
                (
                    username,
                    email,
                    password_hash,
                    datetime.now().isoformat(),
                    is_superuser,
                ),
            )
            conn.commit()
            logger.info(f"Default dev user '{username}' created as superuser.")

