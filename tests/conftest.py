import os

import pytest

@pytest.fixture
def sample_question():
    """Fixture providing a sample question"""
    return """
    Question:
    - A
    - B
    - C
    """

@pytest.fixture
def output_dir():
    """Fixture to ensure output directory exists"""
    os.makedirs("output_data", exist_ok=True)
    yield "output_data"
    # Clean up any test files after tests
    if os.path.exists("output_data/recommendation.md"):
        os.remove("output_data/recommendation.md")
