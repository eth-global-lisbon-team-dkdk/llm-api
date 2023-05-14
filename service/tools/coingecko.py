import requests
from langchain.tools import tool
import requests
from pycoingecko import CoinGeckoAPI
import requests


class CoinGecko:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.currency = "usd"

    def get_price(self, coin: str) -> str:
        """Gets the price of a coin in a currency."""
        price = self.cg.get_price(coin, self.currency)
        return f"The price of {coin} is: ${price}"

    @tool
    def get_market_cap(self, coin: str) -> str:
        """Gets the market cap of a coin."""
        market_cap = self.cg.get_market_cap(coin)
        return f"The market cap of {coin} is: ${market_cap}"

    @tool
    def get_coin_market_chart_by_id(self, coin: str, days: str) -> str:
        """Gets the price of a coin in a currency."""
        market_chart = self.cg.get_coin_market_chart_by_id(coin, self.currency, days)
        return market_chart

    @tool
    def get_coin_market_chart_by_id(self, coin: str, days: str) -> str:
        """Gets the price of a coin in a currency."""
        url = "https://api.coingecko.com/api/v3/coins/" + coin + "/market_chart"
        params = {"vs_currency": self.currency, "days": days, "interval": "daily"}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            return data
        else:
            return "Error:", response.status_code
