from core.decision_engine import DecisionEngine

engine = DecisionEngine()

event = {

    "severity": "Extreme"

}

result = engine.recommend(event)

print(result)