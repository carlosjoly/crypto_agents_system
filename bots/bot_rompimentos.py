import yaml
from core.market_client import CloudMarketClient
from core.indicators import calculate_indicators
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

client = CloudMarketClient()
notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])
tech_params = config["technical_params"]

def run_bot_rompimentos():
    print("Bot D (Rompimentos) iniciado...")
    for symbol in config["market"]["symbols"]:
        prices, volumes = client.get_market_data(symbol)
        df = calculate_indicators(prices, volumes, tech_params["rsi_period"], tech_params["atr_period"])
        
        if df is None or len(df) < 25:
            continue
            
        last_row = df.iloc[-1]
        prev_rows = df.iloc[-21:-1]
        max_high = prev_rows['price'].max()
        
        if last_row['price'] > max_high and last_row['volume_relative'] >= tech_params["volume_spike_multiplier"]:
            mensagem = (
                f"🚀 **ALERTA: Bot D — Rompimento Confirmado por Volume**\n\n"
                f"• Par: `{symbol.upper()}`\n"
                f"• Preço Atual: `{last_row['price']:.4f}` (Resistência anterior: `{max_high:.4f}`)\n"
                f"• Volume Relativo: `{last_row['volume_relative']:.2f}x`"
            )
            notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_rompimentos()
