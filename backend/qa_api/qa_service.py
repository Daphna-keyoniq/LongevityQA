# Business logic
# It does not care whether it's run in an command line or an api

import mimetypes
#from datetime import datetime
# from fastapi import HTTPException

##Internal imports
# from utils.task_manager import TaskManagerRepository, Rating
#from utils.task_status import TaskStatus
#from event_listener import EventListener

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
    def __init__(self):#, task_manager: TaskManagerRepository):
        #self.task_manager = task_manager
        # self.blob_storage = AzureBlobStorage()
        """Initialize the Longevity QA Service."""
        pass

    async def process_question(self, question: str):
        """Process the recommendation in background."""
        # Run recommendation flow
        simple_qa_model = QAModel()
        result = await simple_qa_model.ask(question)
        return result
