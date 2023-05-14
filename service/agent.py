from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import initialize_agent, Tool, AgentType
from service.tools.swap.swap_formatter import SwapFormatter
from langchain.memory import ConversationBufferMemory
from service.tools.thegraph.the_graph import TheGraph
from service.prompt_factory import PromptFactory
from langchain.chat_models import ChatOpenAI
from service.constants import OPEN_AI_KEY
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


class Agent:
    def __init__(self, matic_price_usd: float):
        self.matic_price_usd = matic_price_usd
        self.graph = TheGraph()
        self.swap_formatter = SwapFormatter(self.matic_price_usd)
        llm = ChatOpenAI(
            temperature=0,
            openai_api_key=OPEN_AI_KEY,
            streaming=False,
            callbacks=[StreamingStdOutCallbackHandler()],
            model_name="gpt-4",
        )
        self.prompt_factory = PromptFactory()
        self.memory = ConversationBufferMemory(memory_key="chat_history")

        class CoinPrice(BaseModel):
            address: str = Field(..., description="The coin name to search for.")

        class Swap(BaseModel):
            swap_key: str = Field(
                ...,
                description="The swap key to use to swap token + amount. E.g. to swap $10 of ETH for 'AAVE', swap_key = 'AAVE_10",
            )

        tools = [
            Tool(
                name="Coin Marketcap",
                description="Use this tool to search for crypto market cap of any token. For example, 'What is the market cap of Ethereum?'",
                func=lambda x: "The market cap is $100,000,000,000.",
            ),
            StructuredTool.from_function(
                func=self.graph.main,
                name="The Graph",
                description="Use this tool to search for current crypto prices. For example, 'How much is Ethereum value? or 'What is the price of Ethereum?'",
                args_schema=CoinPrice,
                return_direct=False,
            ),
            StructuredTool.from_function(
                func=self.swap_formatter.format_swap,
                name="Share Swap Schema",
                description="Use this tool to return a JSON swap schema with the client when they request to do a swap or buy a coin. Only respond with JSON that the tool returns to you. Send the tool a string in the format: 'AMOUNT_SYMBOL' e.g '10_AAVE'. This represents user wanting to buy $10 of AAVE.",
                args_schema=Swap,
                return_direct=True,
            ),
        ]
        self.agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=False,
            memory=None,
        )

    def run(self, user_query: str) -> str:
        data = self.agent.run({"input": user_query, "chat_history": None})
        return data
