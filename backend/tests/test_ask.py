import asyncio
import sys
sys.path.append("..")
sys.path.append("../..")
from dotenv import load_dotenv
load_dotenv()

## Internal imports
from qa_model import QAModel


async def test_ask():
    model = QAModel(model_name="longevity_qa_model")
    answer = await asyncio.to_thread(model.ask, "What is longevity?")
    print(answer)

asyncio.run(test_ask())
