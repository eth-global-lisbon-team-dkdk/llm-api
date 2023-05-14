class SwapFormatter:
    def __init__(self, matic_price_usd: float):
        self.matic_price_usd = matic_price_usd

    def map_swap_symbol_to_address(self, swap_symbol):
        swap_symbol = swap_symbol.lower()
        mapping = {
            "grt": "0x5fe2b58c013d7601147dcdd68c143a77499f5531",
            "aave": "0xd6df932a45c0f255f85145f286ea0b292b21c90b",
        }
        return mapping[swap_symbol]

    def format_swap(self, swap_str: str):
        """
        Expects a swap string of the form:
        "10_GRT"
        This indicates user wants to swap ETH for $10 of GRT.
        We split on the underscore and then use this to return a swap dictionary
        """
        swap_str = swap_str.lower()
        amount, symbol = swap_str.split("_")
        amount = float(amount)
        swap_address = self.map_swap_symbol_to_address(symbol)
        swap_amount_matic = round(float(amount / self.matic_price_usd), 2)
        return {
            "address": swap_address,
            "amount_matic": swap_amount_matic,
            "symbol": symbol,
            "is_action": True,
            "action_type": "swap",
            "links": [],
        }
