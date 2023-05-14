from service.model.stream import StreamingChatResponse
from service.prompt_factory import PromptFactory
from service.constants import OPEN_AI_KEY
from service.agent import Agent
from service.utils import get_matic_price


class LLM:
    def __init__(self, temperature: float = 0.0, open_api_key: str = OPEN_AI_KEY):
        self.temperature = temperature
        self.open_api_key = open_api_key
        self.matic_price_usd = get_matic_price()
        self.chat = Agent(self.matic_price_usd)
        self.prompt_factory = PromptFactory()
        self.question_count = 0

    def main(self, query: str) -> str:
        if self.question_count == 3:
            prompt = self.prompt_factory.get_prompt(
                "wallet_connect", wallet_connect=query
            )
        else:
            prompt = self.prompt_factory.get_prompt("regular", intro=query)

        self.question_count += 1

        stream = StreamingChatResponse(
            chat_openai=self.chat,
            temperature=self.temperature,
            open_api_key=self.open_api_key,
        )

        return stream(prompt)
