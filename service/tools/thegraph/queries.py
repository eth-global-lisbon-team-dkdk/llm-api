class Queries:
    QUERY__CURRENT_PRICE = """
    {{
    token(id: "{address}")
    {{
        id
        symbol
        lastPriceUSD
        _totalValueLockedUSD
        }}
    }}
"""
