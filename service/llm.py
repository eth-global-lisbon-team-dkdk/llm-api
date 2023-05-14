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


class LLM:
    def __init__(self, temperature: float = 0.0, open_api_key: str = OPEN_AI_KEY):
        self.temperature = temperature
        self.open_api_key = open_api_key
        self.chat = ChatOpenAI(
            temperature=self.temperature,
            openai_api_key=self.open_api_key,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            model_name="gpt-4",
        )
        self.prompt_factory = PromptFactory()
        self.question_count = 0

    def main(self, query: str) -> str:
        if self.question_count < 2:
            self.question_count += 1
            prompt = self.prompt_factory.get_prompt("intro", intro=query)
        elif self.question_count >= 2:
            prompt = self.prompt_factory.get_prompt(
                "wallet_connect", wallet_connect=query
            )

        stream = StreamingChatResponse(
            chat_openai=self.chat,
            temperature=self.temperature,
            open_api_key=self.open_api_key,
        )

        return stream(prompt).content
