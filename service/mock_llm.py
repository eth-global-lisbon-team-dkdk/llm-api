from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from typing import List
from service.model.stream import StreamingChatResponse

from service.prompt_factory import PromptFactory
from service.constants import OPEN_AI_KEY


class MockLLM:
    def __init__(
        self,
        temperature: float = 0.0,
        open_api_key: str = OPEN_AI_KEY,
        is_cloud_runtime: bool = False,
    ):
        self.temperature = temperature
        self.open_api_key = open_api_key
        self.prompt_factory = PromptFactory(is_cloud_runtime)

    async def main(self, query: str) -> str:
        return {
            "message": "<<LLM Chat Response - will include informational and/or results of tool actions (e.g. Pepe price) and/or links to go and visit>>",
            "chart": {
                "title": "<<title>>",
                "x_axis": "<<x_axis>>",
                "y_axis": "<<y_axis>>",
            },
        }

    async def example(self, query: str) -> str:
        return {
            "message": f"<<LLM Chat Response to question: {query} \n Will include informational and/or results of tool actions (e.g. Pepe price) and/or links to go and visit>>",
            "template": [
                "What is the price of Ethereum?",
                "Where can I buy Ethereum?",
                "What is the difference between Polygon and Ethereum?",
            ],
        }
