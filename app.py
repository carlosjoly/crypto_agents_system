from flask import Flask
import threading
from bots.bot_swing import run_bot_swing
from bots.bot_seguranca import run_bot_seguranca

app = Flask(__name__)

@app.route("/")
def home():
    return "Crypto Agents System 24/7 a funcionar perfeitamente!", 200

@app.route("/run-agents", methods=["GET"])
def trigger_agents():
    # Executa os agentes em background para responder imediatamente ao cron-job
    threading.Thread(target=run_bot_swing).start()
    return {"status": "success", "message": "Agentes acionados com sucesso."}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
