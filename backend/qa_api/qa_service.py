# Business logic
# It does not care whether it's run in an command line or an api

# import os
import mimetypes
# import shutil
# from datetime import datetime
from fastapi import HTTPException
# from typing import Optional
##Internal imports
from utils.task_manager import TaskStatus #Rating, TaskManagerRepository, 
#from event_listener import EventListener
from database import BaseDatabase

## Internal imports
# from main import SimpleQA
from qa_model import QAModel
from utils.logging import get_logger
# from utils.blob_storage import AzureBlobStorage
# Register additional MIME types
mimetypes.add_type("text/markdown", ".md")
mimetypes.add_type("text/csv", ".csv")
mimetypes.add_type("application/json", ".json")

logger = get_logger(__name__)


class LongevityQAService:
    def __init__(self, database: BaseDatabase):#task_manager: TaskManagerRepository):
        #self.task_manager = task_manager
        # self.blob_storage = AzureBlobStorage()
        """Initialize the Longevity QA Service."""
        self.database = database
        self.schema_name = ""

    def _init_table(self) -> None:
        """Initialize task_status table if it doesn't exist."""
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""

        self.database.execute("""DROP TABLE IF EXISTS task_status;""")
        self.database.execute(f"""
            CREATE TABLE IF NOT EXISTS {schema_prefix}task_status (
                task_id SERIAL PRIMARY KEY,
                user_input TEXT,
                status TEXT NOT NULL,
                message TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # # Ensure the `user_input` column exists
        # self.database.execute(f"""
        #     ALTER TABLE {schema_prefix}task_status
        #     ADD COLUMN IF NOT EXISTS user_input TEXT;
        # """)

    async def process_question(self, question: str):
        """Process the recommendation in background."""
        # Run recommendation flow
        model = QAModel(model_name="longevity_qa_model")
        answer = model.ask(question=question)
        return {"answer": answer}

    async def ask_question(self, task_id: int, question: str):
        try:
            # Use the QAModel to process the question
            model = QAModel(model_name="longevity_qa_model")
            answer = model.ask(question=question)

            # Update task status to COMPLETED with the answer
            await self.update_task_status(task_id, status="COMPLETED", message=answer)
        except Exception as e:
            # Update task status to FAILED in case of an error
            await self.update_task_status(task_id, status="FAILED", message=str(e))
            raise

    def get_task_history(self, task_id: int) -> list[TaskStatus]:
        """Get the history of a specific task."""
        schema_prefix = f"{self.schema_name}." if self.schema_name else ""
        rows = self.database.query_all(
            f"""
            SELECT task_id, user_input, status, message, record_entered_timestamp
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
                    task_input=row[1],
                    status=row[2],
                    message=row[3],
                    record_entered_timestamp=row[4],
                )
                for row in rows
            ]
        return []

    async def get_task_status(self, task_id: int):
        """Get status of a specific task."""
        task = self.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def get_task_input(self, task_id: int):
        """Get status of a specific task."""
        task = self.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def create_task(self, user_input:str) -> dict:
        schema_prefix = "" #f"{self.schema_name}." if self.schema_name else ""
        query = f"""
        INSERT INTO {schema_prefix}task_status (user_input, status, message, created_at)
        VALUES (%s, 'PENDING', 'Task created', CURRENT_TIMESTAMP)
        RETURNING task_id;
        """
        task_id = await self.database.query_one(query, (user_input,))
        return {"task_id": task_id, "message": "Task created successfully"}

    async def get_task_by_id(self, task_id: int) -> dict:
        # Fetch task details from the database
        query = "SELECT * FROM task_status WHERE task_id = %s"
        task = await self.database.query_one(query, (task_id,))
        return TaskStatus(
            task_id=task[0],
            task_input=task[1],
            status=task[2],
            message=task[3],
            created_at=task[4],
        ) if task else None

    async def update_task_status(self, task_id: int, status: str, message: str | None = None):
        # Update task status in the database
        query = """
        UPDATE task_status
        SET status = %s, message = %s, updated_at = NOW()
        WHERE task_id = %s
        """
        await self.database.execute(query, (status, message, task_id))

