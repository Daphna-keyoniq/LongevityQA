# filepath: /home/dafne/code/QA_model/src/qa_api/qa_api.py
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn
import sys
import redis
import uuid
sys.path.append("..")
sys.path.append("../..")
from dotenv import load_dotenv

load_dotenv()

## Internal imports
from qa_model import QAModel
from qa_api.qa_service import LongevityQAService
from backend.utils.task_manager import TaskStatus #User,

# # In-memory store (reset on restart, not shared between workers)
# jobs = {}

class InputModel(BaseModel):
    question: str

class OutputModel(BaseModel):
    answer: str

class LongevityQAAPI:
    def __init__(self, longevityqa_service: LongevityQAService):
        self.router = APIRouter(tags=["longevity qa"])
        self.qa_service = longevityqa_service
        self._setup_routes()

    def _setup_routes(self):
        # Add root endpoint
        @self.router.get("/")
        async def read_root():
            """Root endpoint."""
            return {"message": "Welcome to the Longevity QA ChatBot API"}

        @self.router.get("/health")
        async def health_check():
            """Health check endpoint for monitoring."""
            return {"status": "healthy"}

        @self.router.post("/ask", response_model=OutputModel)
        def ask_question(input: InputModel):
            """Endpoint to handle question and return an answer."""
            model = QAModel(model_name="longevity_qa_model")
            answer = model.ask(question=input.question)
            return {"answer": answer}

        @self.router.post("/startask", response_model=OutputModel)
        async def start_ask_question(background_tasks: BackgroundTasks, input: InputModel):
            """Endpoint to handle question and return an answer."""
            result = await self.qa_service.create_task(input.question)
            # Start processing in background
            background_tasks.add_task(
                self.qa_service.process_question,
                int(result["task_id"]),
                result["temp_dir"],
            )
            return {"task_id": result["task_id"], "message": result["message"], "answer": result["answer"]}

        @self.router.post("/tasks/")
        async def create_task(task_id: int, background_tasks: BackgroundTasks):
            background_tasks.add_task(self.qa_service.process_question, task_id)
            return {"message": f"Task {task_id} is being processed in the background."}

        @self.router.get("/task/{task_id}")
        async def get_task_status(task_id: int,) -> TaskStatus:
            return await self.qa_service.get_task_status(task_id)


class LongevityQAServer:
    """Server class handling FastAPI setup and authentication."""

    def __init__(self):
        """Initialize server with configuration."""
        self.limiter = Limiter(key_func=get_remote_address, default_limits=["60/hour"])
        self.app = self.setup_web_app()

    def setup_web_app(self) -> FastAPI:
        """Set up and configure the FastAPI application.

        Returns:
            FastAPI: Configured FastAPI application
        """
        app = FastAPI(
            title="Longevity QA API",
            # TODO: make the api version dynamic
            # TODO: this should only be available in dev
            openapi_url="/api/v1/openapi.json",
            description="API for Longevity Question Answering",
            version="1.0.0",
        )
        app.state.limiter = self.limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

        app.add_middleware(SlowAPIMiddleware)

        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            # In production, replace with specific origins
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        return app

    def add_routes(self, router: APIRouter) -> None:
        """Add routes to the FastAPI application.

        Args:
            router: The APIRouter to add routes from.
        """
        self.app.include_router(router)

    def run(self, port: int = 8011) -> None:
        """Run the FastAPI application."""
        uvicorn.run(self.app, host="0.0.0.0", port=port, reload=False)

