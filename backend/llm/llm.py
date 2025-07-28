from crewai import LLM

DEFAULT_LLM_MODEL = "gemini/gemini-2.0-flash"#"gpt-4o" #"/en/concepts/llms#openai"


def get_deterministic_llm(llm_model: str = DEFAULT_LLM_MODEL) -> LLM:
    """Returns a deterministic LLM model."""
    return LLM(
        model=llm_model,
        temperature=0,
        seed=0,
        n=1,
        max_completion_tokens=16384,
        max_tokens=16384,
        top_p=0,
    )
