import time
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

def run_all():
    print("🚀 A iniciar pipeline completo de verificação dos bots...")
    
    bots = [
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
    
    threads = []
    for bot in bots:
        t = threading.Thread(target=bot)
        threads.append(t)
        t.start()
        
    # Aguarda que todas as threads terminem a execução pontual
    for t in threads:
        t.join()
        
    print("✅ Execução concluída com sucesso. A encerrar processo.")

if __name__ == "__main__":
    run_all()
