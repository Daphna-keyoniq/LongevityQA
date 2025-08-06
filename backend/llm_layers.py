from llm.llm import get_deterministic_llm



def is_longevity_related(question: str) -> bool:
    """
    Check if the question is related to longevity using an LLM filter layer.

    Args:
        question (str): The question to check.

    Returns:
        bool: True if the question is related to longevity, False otherwise.
    """
    # Initialize the LLM
    llm = get_deterministic_llm()

    # Define a prompt or context for the LLM
    prompt = f"""You are given a user input to the longevity question answering system.
    Please determine if the user's input message/question is relevant to longevity medicine. 
    Longevity medicine is a field of medicine that focuses on extending human lifespan and improving healthspan, covering topics accros aging, wellness, lifestyle, disease prevention, and personalised healthcare.
    Longevity interventions and treatments include: medications, repurposed drugs, supplements, lifestyle changes, exercise, nutrition, stress reduction, sleep optimisation, skincare, disease prevention, proactive healthcare, and more.
    If the question is related to longevity, return "True". If the user input is completely unrelated to longevity, return "False". Question: {question}"""

    # Get the response from the LLM
    response = llm(prompt)

    # Check if the LLM predicts a positive response
    return "True" in response.lower()

def is_greeting(question: str) -> bool:
    """
    Check if the question is a greeting.

    Args:
        question (str): The question to check.

    Returns:
        bool: True if the question is a greeting, False otherwise.
    """
    greetings = ["hello", "hi", "hey", "hoi", "what's up"]
    return question.strip().strip("!").strip().lower() in greetings

def is_farewell(question: str) -> bool:
    """
    Check if the question is a farewell.

    Args:
        question (str): The question to check.

    Returns:
        bool: True if the question is a farewell, False otherwise.
    """
    farewells = ["bye", "goodbye", "see you", "take care", "farewell", "good-bye"]
    return question.strip().strip("!").strip().lower() in farewells

