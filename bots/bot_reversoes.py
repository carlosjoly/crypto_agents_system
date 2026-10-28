import yaml
from core.market_client import CloudMarketClient
from core.indicators import calculate_indicators
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

client = CloudMarketClient()
notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])
tech_params = config["technical_params"]

def run_bot_reversoes():
    print("Bot C (Reversões) iniciado...")
    for symbol in config["market"]["symbols"]:
        prices, volumes = client.get_market_data(symbol)
        df = calculate_indicators(prices, volumes, tech_params["rsi_period"], tech_params["atr_period"])
        
        if df is None or len(df) < 5:
            continue
            
        last_row = df.iloc[-1]
        rsi = last_row['rsi']
        vol_rel = last_row['volume_relative']
        price = last_row['price']
        
        if rsi <= tech_params["rsi_oversold"] and vol_rel >= tech_params["volume_spike_multiplier"]:
            mensagem = (
                f"🔄 **ALERTA: Bot C — Possível Reversão de Alta (Fundo)**\n\n"
                f"• Par: `{symbol.upper()}` | Preço: `{price:.4f}`\n"
                f"• RSI (14): `{rsi:.2f}` (Sobrevendido)\n"
                f"• Volume Relativo: `{vol_rel:.2f}x`"
            )
            notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_reversoes()
