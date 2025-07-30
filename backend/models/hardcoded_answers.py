qa_database = {
    "What is longevity?": "Longevity medicine is a field of healthcare that focuses on extending the healthy lifespan of individuals through preventive measures, lifestyle changes, and medical interventions.",
    "What are some tips for healthy aging?": "Some tips for healthy aging include maintaining a balanced diet, staying physically active, engaging in social activities, and managing stress effectively.",
    "What is healthspan?":" Healthspan refers to the period of life during which an individual is generally healthy and free from serious disease, as opposed to lifespan, which is the total length of life.",
    "How can I improve my healthspan?": "To improve your healthspan, focus on regular exercise, a nutritious diet, adequate sleep, mental stimulation, and regular health check-ups.",
    "What is the difference between lifespan and healthspan?": "Lifespan is the total number of years a person lives, while healthspan is the period during which a person remains healthy and free from serious diseases.",
}

def get_hardcoded_answer(question: str) -> str:
    """
    Retrieve a hardcoded answer for the given question.

    Args:
        question (str): The question to retrieve the answer for.

    Returns:
        str: The hardcoded answer if found, otherwise an empty string.
    """
    return qa_database.get(question, "")

