import os
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

# ==============================
# CONFIG
# ==============================

SPACE_DB_API = os.getenv(
    "SPACE_DB_API",
    "https://space-object-database.onrender.com"
)

REQUEST_TIMEOUT = 30

# ==============================
# FASTAPI INIT
# ==============================

app = FastAPI(title="Astra AI - Autonomous Space Intelligence")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# NASA SPACE DB CLIENT
# ==============================

def fetch_from_space_db(endpoint: str, params: dict = None):
    try:
        url = f"{SPACE_DB_API}{endpoint}"
        r = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Space DB API error: {str(e)}")

# ==============================
# INTELLIGENCE ENGINE
# ==============================

def habitability_score(planet: dict):
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

def rank_planets(planets: list):
    for p in planets:
        p["habitability_score"] = habitability_score(p)
    return sorted(planets, key=lambda x: x["habitability_score"], reverse=True)

# ==============================
# CACHE LAYER
# ==============================

@lru_cache(maxsize=32)
def cached_exoplanets(limit: int):
    return fetch_from_space_db("/exoplanets", {"limit": limit})

# ==============================
# ROUTES
# ==============================

@app.get("/")
def root():
    return {"status": "Astra AI Core Online"}

@app.get("/astra/exoplanets")
def get_ranked_exoplanets(limit: int = Query(20, ge=1, le=200)):
    planets = cached_exoplanets(limit)
    return rank_planets(planets)

@app.get("/astra/search")
def search_planets(q: str):
    planets = fetch_from_space_db("/exoplanets/search", {"q": q})
    return rank_planets(planets)

@app.get("/astra/raw")
def raw_data(limit: int = 20):
    return fetch_from_space_db("/exoplanets", {"limit": limit})
