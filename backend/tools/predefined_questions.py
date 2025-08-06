from crewai.tools import BaseTool
from pydantic import BaseModel, Field

## Internal imports
from backend.models.questions_answers import QueryType

class MapAnswersInput(BaseModel):
    """Input schema for GetRelatedRisks."""

    question: str = Field(
        ...,
        description="the question that the user asked",
    )
    query_type : QueryType = Field(
        ...,
        description="the input query that the user asked, and what it was classified as",
    )

class MapAnswers(BaseTool):
    name: str = "Map the predefined answers to certain questions"
    description: str = "You can use this tool when you want to map the predefined answers to certain questions"

    args_schema: type[MapAnswersInput] = MapAnswersInput

    def _run(
        self,
        question: str,
        query_type: QueryType,
    ) -> list:
        if query_type.is_greeting:
            return [
                {
                    "answer": "Hello! How can I help you with your questions about longevity today?",
                }
            ]
        elif query_type.is_qestion_about_system:
            return [
                {
                    "answer": "I am an AI system designed to answer questions about longevity. You can ask me anything related to that topic. I am not a medical professional and cannot provide diagnostics, please consult with your physician for further details.",
                }
            ]
        elif query_type.is_unrelated_question:
            return [
                {
                    "answer": "I'm sorry, I cannot provide that information. I specialize in answering questions about longevity medicine. If you have a question related to that topic, feel free to ask!",
                }
            ]

        else:
            return {}
