import yaml
from notifications.telegram_bot import TelegramNotifier

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

notifier = TelegramNotifier(config["telegram"]["token"], config["telegram"]["chat_id"])

class FundamentalEvaluator:
    def __init__(self, weights):
        self.weights = weights

    def evaluate_project(self, project_data):
        scores = project_data.get("scores", {})
        red_flags = project_data.get("red_flags", [])
        
        total_score = sum(scores.get(cat, 0) * (w / 100.0) for cat, w in self.weights.items())
        is_rejected = len(red_flags) > 0 or total_score < 60.0
        confidence = "Alta" if total_score >= 80 else ("Média" if total_score >= 65 else "Baixa")

        return {
            "total_score": round(total_score, 1),
            "confidence": confidence,
            "is_rejected": is_rejected,
            "red_flags": red_flags
        }

def run_bot_fundamental():
    weights = config["fundamental_weights"]
    evaluator = FundamentalEvaluator(weights)
    
    sample_project = {
        "name": "Project Alpha (PALPHA)",
        "scores": {
            "utility_quality": 85,
            "team_execution": 70,
            "tokenomics_unlocks": 80,
            "adoption_onchain": 60,
            "security_transparency": 90,
            "organic_social_interest": 75
        },
        "red_flags": []
    }

    result = evaluator.evaluate_project(sample_project)
    if not result["is_rejected"]:
        mensagem = (
            f"📊 **ALERTA: Bot H — Avaliação Fundamentalista**\n\n"
            f"• Projeto: `{sample_project['name']}`\n"
            f"• **Pontuação Final:** `{result['total_score']}/100`\n"
            f"• Nível de Confiança: `{result['confidence']}`"
        )
        notifier.send_alert(mensagem)

if __name__ == "__main__":
    run_bot_fundamental()
