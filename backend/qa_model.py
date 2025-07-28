import uuid

# from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start

# # Importing AI Suite for adhoc LLM calls and Pydantic
from pydantic import BaseModel


##Internal imports
from crews.simple_qa_crew.qa_crew import SimpleQACrew
from models.outputs import Answer
from utils.logging import get_logger

# import aisuite as ai

# urls = [
#     "https://lilianweng.github.io/posts/2023-06-23-agent/",
#     "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
#     "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
# ]

# research_agent = Agent(
#     role="You are a helpful assistant that can answer questions about the web.",
#     goal="Answer the user's question.",
#     backstory="You have access to a vast knowledge base of information from the web.",
#     tools=[
#       WebsiteSearchTool(website=urls[0]),
#       WebsiteSearchTool(website=urls[1]),
#       WebsiteSearchTool(website=urls[2]),
#     ],
#     llm="gpt-4o-mini",
# )

# task = Task(
#   description="Answer the following question: {question}",
#   expected_output="A detailed and accurate answer to the user's question.",
#   agent=research_agent,
# )

# crew = Crew(
#     agents=[research_agent],
#     tasks=[task],
# )

# # A simple dictionary-based QA model
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
  async def process_question(self):
    self.logger.info("Processing question")

    qa_crew = SimpleQACrew()
    input_parser_result: Answer = await qa_crew.kickoff(inputs={"question": self.state.question})
    self.state.answer = input_parser_result.pydantic

    self.logger.info("Processing input completed")

    return self.state.answer

    # @listen(process_question)
    # def answer_question(self):
    #     print(f"# Answering question: {self.state.improved_question}")
    #     result = crew.kickoff(inputs={'question': self.state.improved_question})
    #     self.state.answer = result.raw
    #     return result

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
        self.logger.info("Got response", extra={"answer": results})
        return results.answer

