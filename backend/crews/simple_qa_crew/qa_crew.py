from pathlib import Path
# CreqAI imports
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.tasks.conditional_task import ConditionalTask

## Internal imports
# crews
from crews.simple_qa_crew.guardrail import validate_and_trasform
# models
from backend.models.questions_answers import Answer, Question

# tools
from llm.llm import get_deterministic_llm, get_gemini_llm, get_mistral_llm
from utils.logging import log_execution_time, get_logger
from config import Config
config = Config().load_configuration()
logger = get_logger(__name__)


def is_supplement_question(question: Question) -> bool:
    """
    Check if the question is related to supplement knowledge.
    This is a placeholder function. You can implement your own logic.
    """
    # Example logic: check if the question contains specific keywords
    return any(keyword.lower() in question.pydantic.labels for keyword in ["supplement", "supplements", "vitamins"])

def is_disease_question(question: Question) -> bool:
    """
    Check if the question is related to supplement knowledge.
    This is a placeholder function. You can implement your own logic.
    """
    # Example logic: check if the question contains specific keywords
    if not question or not question.pydantic:
        return False
    if not hasattr(question.pydantic, 'labels'):
        logger.warning(f"Question does not have labels: {question}")
        return False
    logger.info(f"Checking if question is disease related: {question}, {question.pydantic}")
    return any(keyword.lower() in question.pydantic.labels for keyword in ["disease", "condition", "risk"])

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

    # supplement_knowledge_folder = Path(
    #     config.paths.full_knowledge_dir
    #     / "supplements/processed_papers_and_guidelines/clean_texts"
    # )

    # supplement_file_paths = list(Path(supplement_knowledge_folder).glob("*.txt"))  # noqa

    # supplement_text_source = TextFileKnowledgeSource(
    #     file_paths=supplement_file_paths,
    #     chunk_size=10000,
    #     chunk_overlap=1000,
    # )

    # # disease_knowledge_folder = Path(
    #     config.paths.full_knowledge_dir
    #     / "disease_management/clean_texts"
    # )

    # disease_file_paths = list(Path(disease_knowledge_folder).glob("*.txt"))  # noqa

    # disease_text_source = TextFileKnowledgeSource(
    #     file_paths=disease_file_paths,
    #     chunk_size=10000,
    #     chunk_overlap=1000,
    # )

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
        )

    @agent
    def question_labelling_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["question_labelling_agent"],  # type: ignore
            llm=self.llm,
            verbose=True,
        )

    @agent
    def knowledge_processing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["knowledge_processing_agent"],  # type: ignore
            llm=self.llm,
            verbose=True,
            max_retry_limit=1,        )

    @agent
    def question_answering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["question_answering_agent"],  # type: ignore
            llm=self.llm_gemini,
            fallback_llm=self.llm_mistral,
            verbose=True,
            max_retry_limit=1,
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
    def query_type_task(self) -> Task:
        return Task(
            config=self.tasks_config["query_type_task"],  # type: ignore
            output_pydantic=Question,
            guardrail=validate_and_trasform,
            max_retries=0,
        )

    @task
    def question_labelling_task(self) -> Task:
        return Task(
            config=self.tasks_config["question_filtering_task"],  # type: ignore
            output_pydantic=Question,
            context=[self.question_filtering_task()],  # type: ignore
            guardrail=validate_and_trasform,
            max_retries=0,
        )

    # @task
    # def supplement_knowledge_task(self) -> ConditionalTask:
    #     """Task to process the supplement knowledge source"""
    #     conditional_task = ConditionalTask(
    #         config=self.tasks_config["supplement_knowledge_task"],  # type: ignore
    #         knowledge_sources=[self.supplement_text_source],
    #         context=[self.question_labelling_task()],
    #         output_pydantic=Question,
    #         condition=is_supplement_question,
    #         guardrail=validate_and_trasform,
    #         max_retries=0,
    #     )
    #     self.logger.info("Conditional supplement knowledge task created")
    #     return conditional_task

    # @task
    # def disease_knowledge_task(self) -> ConditionalTask:
    #     """Task to process the supplement knowledge source"""
    #     conditional_task = ConditionalTask(
    #         config=self.tasks_config["disease_knowledge_task"],  # type: ignore
    #         knowledge_sources=[self.disease_text_source],
    #         context=[self.question_labelling_task()],
    #         output_pydantic=Question,
    #         condition=is_disease_question,
    #         max_retries=0,
    #     )
    #     self.logger.info("Conditional supplement knowledge task created")
    #     return conditional_task

    @task
    def question_answering_task(self) -> Task:
        return Task(
            config=self.tasks_config["question_answering_task"],  # type: ignore
            context=[self.question_labelling_task()],  # type: ignore
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
            # manager_llm=self.llm,  # LLM used for the crew manager
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

