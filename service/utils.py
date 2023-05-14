import requests


def get_matic_price():
    response = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd"
    )

    if response.status_code == 200:
        data = response.json()
        return round(float(data["matic-network"]["usd"]), 2)
    else:
        return 0.88
