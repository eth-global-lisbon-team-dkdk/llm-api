from service.tools.thegraph.query_formatter import QueryFormatter
from typing import Any
import requests


class TheGraph:
    def __init__(
        self, url="https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum"
    ):
        self.url = url
        self.query_formatter = QueryFormatter()

    def map_symbol_to_address(self, symbol: str) -> str:
        symbol = symbol.lower()
        mapping = {
            "grt": "0xc944e90c64b2c07662a292be6244bdf05cda44a7",
            "usdc": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "usdt": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "dai": "0x6b175474e89094c44da98b954eedeac495271d0f",
        }
        return mapping[symbol]

    def get(self, query: str) -> Any:
        r = requests.post(self.url, json={"query": query})
        return r.json()

    def transform(self, result: dict, query_key: str):
        if query_key == "current_price_usd":
            result = {
                "address": result["data"]["token"]["id"],
                "price_usd": round(float(result["data"]["token"]["lastPriceUSD"]), 5),
                "symbol": result["data"]["token"]["symbol"],
            }
        return result

    def main(self, symbol: str, query_key: str = None):
        address = self.map_symbol_to_address(symbol)
        if query_key is None:
            query = self.query_formatter.gql_queries["current_price_usd"]
        else:
            query = self.query_formatter.gql_queries[query_key]
        formatted_query = self.query_formatter.format_query(query, address)
        result = self.get(formatted_query)
        result = self.transform(result, query_key)
        return result
