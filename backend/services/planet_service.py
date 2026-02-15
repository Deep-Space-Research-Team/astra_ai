from backend.database import SessionLocal
from backend.models import Exoplanet

def get_ranked_planets(limit=20):
    session = SessionLocal()
    planets = session.query(Exoplanet)\
        .order_by(Exoplanet.habitability_score.desc())\
        .limit(limit).all()
    session.close()
    return planets
