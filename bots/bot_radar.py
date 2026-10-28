import yaml
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])

def run_bot_radar():
    print("Bot F (Radar de Lançamentos) a executar varredura...")
    # Lógica de varredura de novos tokens ou pares recém-incorporados nas APIs de listagem
    # Exemplo simulado de descoberta estruturada:
    novo_token_detectado = None  # Atribuir se detetar novo ativo nas fontes configuradas
    
    if novo_token_detectado:
        mensagem = (
            f"💎 **ALERTA: Bot F — Novo Lançamento/Listagem Detetado**\n\n"
            f"• Ativo: `{novo_token_detectado}`\n"
            f"• Status: Em fase de triagem inicial para auditoria fundamentalista."
        )
        notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_radar()
