from backend.database import SessionLocal
from backend.models import Exoplanet
from backend.clients.nasa_client import fetch_exoplanets
from backend.intelligence.habitability import calculate_habitability

def update_exoplanets():
    session = SessionLocal()

    planets = fetch_exoplanets(500)

    for p in planets:
        score = calculate_habitability(p)

        obj = Exoplanet(
            name=p.get("name"),
            host_star=p.get("host_star"),
            orbital_period_days=p.get("orbital_period_days"),
            radius_earth=p.get("radius_earth"),
            mass_earth=p.get("mass_earth"),
            discovery_method=p.get("discovery_method"),
            discovery_year=p.get("discovery_year"),
            habitability_score=score
        )

        session.merge(obj)

    session.commit()
    session.close()
