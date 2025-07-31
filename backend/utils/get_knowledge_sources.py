from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

from pathlib import Path

## Internal imports
from config import Config

config = Config().load_configuration()

def get_supplement_info()->TextFileKnowledgeSource:
    supplement_knowledge_folder = Path(
        config.paths.full_knowledge_dir
        / "supplements/processed_papers_and_guidelines/clean_texts"
    )

    supplement_file_paths = list(Path(supplement_knowledge_folder).glob("*.txt"))  # noqa

    supplement_text_source = TextFileKnowledgeSource(
        file_paths=supplement_file_paths,
        chunk_size=10000,
        chunk_overlap=1000,
    )
    return supplement_text_source

def get_disease_info()->TextFileKnowledgeSource:
    """
    Returns a TextFileKnowledgeSource for disease management knowledge.
    """
    disease_knowledge_folder = Path(
        config.paths.full_knowledge_dir
        / "disease_management/clean_texts"
    )

    disease_file_paths = list(Path(disease_knowledge_folder).glob("*.txt"))  # noqa

    disease_text_source = TextFileKnowledgeSource(
        file_paths=disease_file_paths,
        chunk_size=10000,
        chunk_overlap=1000,
    )
    return disease_text_source