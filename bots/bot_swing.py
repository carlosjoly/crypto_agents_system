import yaml
from core.market_client import CloudMarketClient
from core.indicators import calculate_indicators
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

client = CloudMarketClient()
notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])
tech_params = config["technical_params"]

def run_bot_swing():
    print("Bot E (Swing Trade) a executar verificação...")
    for symbol in config["market"]["symbols"]:
        prices, volumes = client.get_market_data(symbol)
        df = calculate_indicators(prices, volumes, tech_params["rsi_period"], tech_params["atr_period"])
        
        if df is None or len(df) < 5:
            continue
            
        last_row = df.iloc[-1]
        price = last_row['price']
        rsi = last_row['rsi']
        atr = last_row['atr']
        vol_rel = last_row['volume_relative']
        
        # Estratégia de recuo em tendência com volume saudável
        if rsi <= tech_params["rsi_oversold"] and vol_rel >= tech_params["volume_spike_multiplier"]:
            stop_loss = price - (1.5 * atr)
            target = price + (3.0 * atr)
            rr = (target - price) / (price - stop_loss)
            
            msg = (
                f"🎯 **ALERTA: Bot E — Oportunidade de Swing Trade**\n\n"
                f"• Ativo: `{symbol.upper()`}\n"
                f"• Preço Atual: `{price:.4f}`\n"
                f"• RSI (14): `{rsi:.2f}` (Zona de Sobrevenda / Recuo)\n"
                f"• Volume Relativo: `{vol_rel:.2f}x`\n\n"
                f"📋 **Plano Manual:**\n"
                f"• Entrada: `{price:.4f}`\n"
                f"• Stop Loss: `{stop_loss:.4f}`\n"
                f"• Alvo: `{target:.4f}`\n"
                f"• Risco/Retorno: `1:{rr:.2f}`"
            )
            notifier.send_alert(msg)

if __name__ == "__main__":
    run_bot_swing()
