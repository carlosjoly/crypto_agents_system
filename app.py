from flask import Flask
import threading

# Importação dos 10 bots do sistema
from bots.bot_altas import run_bot_altas
from bots.bot_quedas import run_bot_quedas
from bots.bot_reversoes import run_bot_reversoes
from bots.bot_rompimentos import run_bot_rompimentos
from bots.bot_swing import run_bot_swing
from bots.bot_radar import run_bot_radar
from bots.bot_social import run_bot_social
from bots.bot_fundamental import run_bot_fundamental
from bots.bot_seguranca import run_bot_seguranca
from bots.bot_tokenomics import run_bot_tokenomics

app = Flask(__name__)

@app.route("/")
def home():
    return "Sistema Completo de 10 Bots de Criptomoedas a operar 24/7 na Nuvem!", 200

def trigger_all_bots():
    bots_list = [
        run_bot_altas,
        run_bot_quedas,
        run_bot_reversoes,
        run_bot_rompimentos,
        run_bot_swing,
        run_bot_radar,
        run_bot_social,
        run_bot_fundamental,
        run_bot_tokenomics
    ]
    
    for bot_func in bots_list:
        try:
            threading.Thread(target=bot_func).start()
        except Exception as e:
            print(f"Erro ao disparar bot: {e}")

@app.route("/run-agents", methods=["GET"])
def run_agents_endpoint():
    trigger_all_bots()
    return {"status": "success", "message": "Todos os agentes independentes foram acionados em paralelo."}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
