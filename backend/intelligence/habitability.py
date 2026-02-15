def calculate_habitability(planet):
    score = 0

    r = planet.get("radius_earth")
    m = planet.get("mass_earth")
    p = planet.get("orbital_period_days")

    if r and 0.8 <= r <= 1.5:
        score += 40

    if m and 0.5 <= m <= 5:
        score += 30

    if p and 200 <= p <= 400:
        score += 30

    return score
