import requests

class CloudMarketClient:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_market_data(self, coin_id="bitcoin"):
        url = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": "1"}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                prices = data.get("prices", [])
                volumes = data.get("total_volumes", [])
                return prices, volumes
        except Exception as e:
            print(f"Erro ao consultar dados de mercado para {coin_id}: {e}")
        return [], []
