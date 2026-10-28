import requests

class GoPlusSecurityChecker:
    @staticmethod
    def check_token_security(chain_id: str, contract_address: str):
        # chain_id 1 = Ethereum, 56 = BSC, solana = Solana endpoint específico
        url = f"https://api.gopluslabs.io/api/v1/token_security/{chain_id}"
        params = {"contract_addresses": contract_address}
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                result = response.json().get("result", {})
                token_data = result.get(contract_address.lower(), {})
                
                is_honeypot = token_data.get("is_honeypot", "0") == "1"
                buy_tax = float(token_data.get("buy_tax", 0))
                sell_tax = float(token_data.get("sell_tax", 0))
                owner_changeable = token_data.get("cannot_sell_all", "0") == "1"
                
                return {
                    "safe": not is_honeypot and buy_tax < 10 and sell_tax < 10 and not owner_changeable,
                    "is_honeypot": is_honeypot,
                    "buy_tax": buy_tax,
                    "sell_tax": sell_tax,
                    "risk_details": token_data
                }
        except Exception as e:
            print(f"Erro na consulta GoPlus Security: {e}")
        return {"safe": False, "error": "Falha na API de Segurança"}
