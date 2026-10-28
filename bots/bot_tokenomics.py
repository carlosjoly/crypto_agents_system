import yaml
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])

def run_bot_tokenomics():
    print("Bot J (Tokenomics) a analisar métricas...")
    token_symbol = "NEWCOIN"
    mcap = 50000000
    fdv = 500000000
    circulating_pct = 10.0
    
    high_inflation_risk = circulating_pct < 25.0
    ratio_fdv = fdv / mcap if mcap > 0 else 0

    mensagem = (
        f"🪙 **ALERTA: Bot J — Análise de Tokenomics**\n\n"
        f"• Token: `{token_symbol}`\n"
        f"• Market Cap: `${mcap:,.0f}` | FDV: `${fdv:,.0f}`\n"
        f"• Oferta Circulante: `{circulating_pct:.1f}%`\n"
        f"• Risco de Inflação Futura: `{'ELEVADO (Desbloqueios agressivos)' if high_inflation_risk else 'Baixo'}`"
    )
    notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_tokenomics()
