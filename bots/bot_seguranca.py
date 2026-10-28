import yaml
from core.goplus_security import GoPlusSecurityChecker
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])

def run_bot_seguranca(chain_id, contract_address, token_name):
    print(f"Bot I (Segurança GoPlus) a auditar {token_name}...")
    sec = GoPlusSecurityChecker.check_token_security(chain_id, contract_address)
    
    if not sec.get("safe", False):
        msg = (
            f"🛡️ **ALERTA DE SEGURANÇA: Bot I — Risco Detetado**\n\n"
            f"• Token: `{token_name}`\n"
            f"• Contrato: `{contract_address}`\n"
            f"• É Honeypot?: `{'SIM 🚨'}`\n"
            f"• Imposto Compra/Venda: `{sec.get('buy_tax', 0)}% / {sec.get('sell_tax', 0)}%`\n\n"
            f"❌ **Diagnóstico:** Rejeitado por falhas severas de segurança."
        )
        notifier.send_alert(msg)

if __name__ == "__main__":
    # Exemplo de auditoria na rede BSC (chain_id: 56)
    run_bot_seguranca("56", "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c", "WBNB (Exemplo)")
