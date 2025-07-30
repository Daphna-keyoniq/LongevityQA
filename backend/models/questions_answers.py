from pydantic import BaseModel


class QueryType(BaseModel):
    query: str
    is_greeting: bool = False
    is_longevity_related: bool = False
    is_qestion_about_system: bool = False
    is_unrelated_question: bool = False
    is_other: bool = False

class Question(BaseModel):
    question: str
    is_longevity_related: bool = True
    labels: list[str] = []

class Answer(BaseModel):
    answer: str
