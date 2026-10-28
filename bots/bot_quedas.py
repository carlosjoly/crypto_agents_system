import yaml
from core.market_client import CloudMarketClient
from core.indicators import calculate_indicators
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

client = CloudMarketClient()
notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])
tech_params = config["technical_params"]

def run_bot_quedas():
    print("Bot B (Quedas Expressivas) iniciado...")
    for symbol in config["market"]["symbols"]:
        prices, volumes = client.get_market_data(symbol)
        df = calculate_indicators(prices, volumes, tech_params["rsi_period"], tech_params["atr_period"])
        
        if df is None or len(df) < 2:
            continue
            
        close_prev = df.iloc[-2]['price']
        close_curr = df.iloc[-1]['price']
        var_pct = ((close_curr - close_prev) / close_prev) * 100
        
        if var_pct <= -tech_params["price_change_threshold_pct"]:
            mensagem = (
                f"📉 **ALERTA: Bot B — Queda Expressiva Detetada**\n\n"
                f"• Ativo: `{symbol.upper()}`\n"
                f"• Preço Atual: `{close_curr:.4f}`\n"
                f"• Variação: `{var_pct:.2f}%`\n"
                f"• Motivo: Pressão vendedora anómala."
            )
            notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_quedas()
