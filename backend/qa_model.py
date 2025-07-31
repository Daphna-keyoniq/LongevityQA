import uuid

# from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start

# # Importing AI Suite for adhoc LLM calls and Pydantic
from pydantic import BaseModel


##Internal imports
from crews.simple_qa_crew.qa_crew import SimpleQACrew
from crews.question_parsing_crew.question_crew import QuestionParsingCrew
from backend.models.questions_answers import Answer, Question
from utils.logging import get_logger

class QAState(BaseModel):
  """
  State for the documentation flow
  """
  question: str = "What is longevity?"
  question_parsed: Question = Question(
      question="What is longevity?",
      is_longevity_related=True,
      query_type="longevity question",
      )
  improved_question: str = ""
  answer: str = ""
  request_id: int = 0

class LongevityQAFlow(Flow[QAState]):

  def __init__(self, question: str = "What is longevity?", **kwargs):
     super().__init__()
     self.state.question = question
     self.state.request_id = str(uuid.uuid4())
     self.logger = get_logger(__name__)
     self.logger.info(
            "LongevityQAFlow initialized",
            extra={"request_id": self.state.request_id},
        )

  @start()
  def process_question(self):
    self.logger.info("Processing question")

    input_crew = QuestionParsingCrew()
    question_parsed: Question = input_crew.kickoff(inputs={"question": self.state.question})
    self.state.question_parsed = question_parsed.pydantic

    # qa_crew = SimpleQACrew()
    # answer: Answer = qa_crew.kickoff(inputs={"question": self.state.question})
    # self.state.answer = answer.pydantic

    self.logger.info("Processing input completed")
    return self.state

  @listen(process_question)
  def answer_question(self):
      qa_crew = SimpleQACrew()
      answer: Answer = qa_crew.kickoff(inputs={"question": self.state.question_parsed.model_dump_json()})
      self.state.answer = answer.pydantic
      self.state.answer_str = str(answer.answer)

      self.logger.info("Answer Completed",)
      return self.state

class QAModel:
    def __init__(self, model_name: str):
        """Initialize the QA model with a specified model name."""
        self.model_name = model_name
        self.logger = get_logger(__name__)

    def add_knowledge(self, question: str, answer: str):
        """Add a question and its answer to the QA database."""
        self.qa_database[question] = answer

    def ask(self, question: str) -> str:
        """
        Retrieve the answer to a question from the QA database.

        This method uses the LongevityQAFlow class to process the question
        and generate an answer.
        """
        qa_flow = LongevityQAFlow(question=question)
        self.logger.info("Starting QA flow", extra={"question": question})
        #input_state = QAState(question=question)
        results = qa_flow.kickoff()
        self.logger.info("Got response", extra={"answer": results.answer.answer})
        return results.answer_str

