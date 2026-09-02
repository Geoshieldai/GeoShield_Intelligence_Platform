from core.risk_engine import RiskEngine

engine = RiskEngine()

fire = {

    "brightness": 367,

    "frp": 12.6,

    "confidence": "h"

}

risk = engine.calculate_fire_risk(fire)

print(risk)