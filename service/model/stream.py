from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from service.constants import OPEN_AI_KEY
from typing import List


class StreamingChatResponse:
    def __init__(
        self,
        chat_openai: ChatOpenAI,
        temperature: float = 0.0,
        open_api_key: str = OPEN_AI_KEY,
    ):
        self.chat = chat_openai
        self.open_api_key = open_api_key
        self.temperature = temperature

    def process_message(self, human_message: str) -> str:
        return self.chat([human_message])

    def process_messages(self, messages: List[str]) -> List[str]:
        return self.chat(messages)

    def __call__(self, human_message: HumanMessage):
        return self.chat.run([HumanMessage(content=human_message)])
