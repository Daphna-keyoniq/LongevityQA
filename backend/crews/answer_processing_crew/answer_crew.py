from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

## Internal imports
# crews
from crews.simple_qa_crew.guardrail import validate_and_trasform
# models
from backend.models.questions_answers import Answer, Question

# tools
from llm.llm import get_deterministic_llm, get_gemini_llm, get_mistral_llm
from utils.logging import log_execution_time, get_logger


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
@CrewBase
class SimpleQACrew:
    """Simple Vanilla QA Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = get_deterministic_llm()
    llm_gemini = get_gemini_llm()
    llm_mistral = get_mistral_llm()

    name = "Simple QA Crew"

    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info("SimpleQACrew initialized")

    @agent
    def question_filtering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["question_filtering_agent"],  # type: ignore
            llm=self.llm,
            verbose=True,
            max_retry_limit=5,
        )

    @agent
    def question_answering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["question_answering_agent"],  # type: ignore
            llm=self.llm_mistral,
            verbose=True,
            max_retry_limit=5,
        )

    @task
    def question_filtering_task(self) -> Task:
        return Task(
            config=self.tasks_config["question_filtering_task"],  # type: ignore
            output_pydantic=Question,
            guardrail=validate_and_trasform,
            max_retries=0,
        )

    @task
    def question_answering_task(self) -> Task:
        return Task(
            config=self.tasks_config["question_answering_task"],  # type: ignore
            context=[self.question_filtering_task()],  # type: ignore
            output_pydantic=Answer,
            guardrail=validate_and_trasform,
            max_retries=0,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator # type: ignore
            tasks=self.tasks,  # Automatically created by the @task decorator # type: ignore
            process=Process.sequential,
            verbose=True,
            # output_log_file="logs/crews/simple_qa_crew.json",  # if log_path is False, then no log file will be created
            name=self.name,
        )

    @log_execution_time
    def kickoff(self, inputs: dict, **kwargs):
        """Override kickoff to add input validation"""
        self.logger.info(
            "Starting Simple QA Crew kickoff",
            extra={"input_keys": list(inputs.keys())},
        )
        try:
            result = self.crew().kickoff(inputs=inputs, **kwargs)
            self.logger.info("Simple QA Crew kickoff completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Simple QA Crew kickoff failed: {e!s}", exc_info=True)
            raise

