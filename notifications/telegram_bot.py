import os
import requests

class TelegramNotifier:
    def __init__(self, token=None, chat_id=None):
        # Lê prioritariamente das variáveis de ambiente do Render; se não encontrar, usa os argumentos
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.token or not self.chat_id:
            print("⚠️ Aviso: Credenciais do Telegram não configuradas nas variáveis de ambiente.")
            
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_alert(self, message):
        if not self.token or not self.chat_id:
            print("Erro: Impossível enviar alerta, token ou chat_id em falta.")
            return False
            
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(self.base_url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao enviar alerta para o Telegram: {e}")
            return False
