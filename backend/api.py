
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(".")
load_dotenv()

## Internal imports
from qa_api.qa_api import LongevityQAAPI, LongevityQAServer
from qa_api.qa_service import LongevityQAService
from config import Config
from utils.task_manager import TaskManagerRepository
from database.postgres_database import PostgresDatabase
config = Config().load_configuration(type="prod")

def setup():
    # Initialize dependencies
    database = PostgresDatabase(**config.database.db_config)
    #task_manager = TaskManagerRepository(database)

    # Create server
    server = LongevityQAServer()

    # Create business services
    service = LongevityQAService(database)

    # Api endpoints
    api = LongevityQAAPI(service)

    # Register api endpoints on the server
    server.add_routes(api.router)

    return server

server = setup()
app = server.app

if __name__ == "__main__":
    # Run the server
    # Create the app instance for Gunicorn or FastAPI to use
    server.run()
