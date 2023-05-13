from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from typing import List

from service.model.stream import StreamingChatResponse
from service.constants import OPEN_AI_KEY


class LLM:
    def __init__(self, temperature: float = 0.0, open_api_key: str = OPEN_AI_KEY):
        self.temperature = temperature
        self.open_api_key = open_api_key
        self.chat = ChatOpenAI(
            temperature=self.temperature,
            openai_api_key=self.open_api_key,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )

    def main(self, query: str) -> str:
        stream = StreamingChatResponse(
            chat_openai=self.chat,
            temperature=self.temperature,
            open_api_key=self.open_api_key,
        )
        return stream(query)
