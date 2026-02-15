from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Exoplanet(Base):
    __tablename__ = "exoplanets"

    name = Column(String, primary_key=True)
    host_star = Column(String)
    orbital_period_days = Column(Float)
    radius_earth = Column(Float)
    mass_earth = Column(Float)
    discovery_method = Column(String)
    discovery_year = Column(Integer)
    habitability_score = Column(Float)
