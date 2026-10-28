import yaml
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])

def run_bot_social():
    print("Bot G (Inteligência Social) a recolher métricas...")
    # Simulação de análise de buzz social / menções
    token_symbol = "SOL"
    social_score = 82
    volume_change_pct = 65.4
    
    if volume_change_pct >= 50.0 and social_score >= 70:
        mensagem = (
            f"🗣️ **ALERTA: Bot G — Pico de Interesse Social Detetado**\n\n"
            f"• Token: `{token_symbol}`\n"
            f"• Sentimento Social: `{social_score}/100`\n"
            f"• Crescimento de Menções: `+{volume_change_pct:.1f}%`"
        )
        notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_social()
