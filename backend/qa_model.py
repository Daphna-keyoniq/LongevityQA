import uuid

# from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start

# # Importing AI Suite for adhoc LLM calls and Pydantic
from pydantic import BaseModel


##Internal imports
from crews.simple_qa_crew.qa_crew import SimpleQACrew
#from crews.question_parsing_crew.question_crew import QuestionParsingCrew
from backend.models.questions_answers import Answer
from utils.logging import get_logger
from backend.llm_layers import is_greeting, is_farewell

class QAState(BaseModel):
  """
  State for the documentation flow
  """
  question: str = "What is longevity?"
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

    qa_crew = SimpleQACrew()
    answer: Answer = qa_crew.kickoff(inputs={"question": self.state.question})
    self.state.answer = answer.pydantic

    self.logger.info("Processing input completed")
    return self.state.answer

class QAModel:
    def __init__(self, model_name: str):
        """Initialize the QA model with a specified model name."""
        self.model_name = model_name
        self.logger = get_logger(__name__)

    def ask(self, question: str) -> str:
        """
        Retrieve the answer to a question from the QA database.

        This method uses the LongevityQAFlow class to process the question
        and generate an answer.
        """
        self.logger.info(f"Received question: {question}")
        if is_greeting(question):
          self.logger.info("Detected greeting in question")
          answer = """Hello! I am a longevity medicine question answering agent. I can help you with questions about improving healthspan, proactive health and related topics. What would you like to know?"""
          return answer

        elif is_farewell(question):
          self.logger.info("Detected farewell in question")
          answer = """Goodbye! Have a great day!"""
          return answer
        
        qa_flow = LongevityQAFlow(question=question)
        self.logger.info("Starting QA flow", extra={"question": question})
        #input_state = QAState(question=question)
        results = qa_flow.kickoff()
        self.logger.info("Got response", extra={"answer": results})
        return results.answer

    def ask2(self, question:str) -> str:
       answer = question

       return answer

