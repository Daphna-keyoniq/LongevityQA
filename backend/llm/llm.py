from crewai import LLM

DEFAULT_LLM_MODEL = "gpt-4o"#"gemini/gemini-2.0-flash" #"google/gemma-3-12b-it"#"llama-3_3-Nemotron-Super-49B-v1" #"gemini/gemini-2.0-flash"#"gpt-4o" #"/en/concepts/llms#openai"


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

def get_gemini_llm() -> LLM:
    """Returns a deterministic LLM model."""
    return LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0,
        seed=0,
        n=1,
        max_completion_tokens=16384,
        max_tokens=16384,
        top_p=0,
    )

def get_mistral_llm() -> LLM:
    """Returns a deterministic LLM model."""
    return LLM(
        model="mistral/mistral-large-latest", #"perplexity/perplexity-llama-3.1-70b",
        temperature=0,
        seed=0,
        n=1,
        max_completion_tokens=16384,
        max_tokens=16384,
        top_p=0,
    )