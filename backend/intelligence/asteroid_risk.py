def asteroid_risk_score(obj):
    score = 0
    if obj.get("diameter") and obj["diameter"] > 1000:
        score += 50
    return score
