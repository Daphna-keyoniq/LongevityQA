# filepath: /home/dafne/code/QA_model/src/qa_api/qa_api.py
from pydantic import BaseModel
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn
import sys
sys.path.append("..")
sys.path.append("../..")
from dotenv import load_dotenv

load_dotenv()

## Internal imports
from qa_model import QAModel
# from qa_api.qa_service import LongevityQAService


class InputModel(BaseModel):
    question: str

class OutputModel(BaseModel):
    answer: str

class LongevityQAAPI:
    def __init__(self):
        self.router = APIRouter(tags=["longevity qa"])
        # self.qa_service = longevityqa_service
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
        async def ask_question(input: InputModel):
                """Endpoint to handle question and return an answer."""
                model = QAModel(model_name="longevity_qa_model")
                answer = model.ask(question=input.question)
                return {"answer": answer}

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

