def detect_anomaly(planet):
    if planet.get("radius_earth") and planet["radius_earth"] > 20:
        return True
    return False
