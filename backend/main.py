import os
import requests
from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

SPACE_DB_URL = os.getenv("SPACE_DB_URL")

if not SPACE_DB_URL:
    raise RuntimeError("SPACE_DB_URL not set")

app = FastAPI(title="Astra AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# =====================================================
# ROOT
# =====================================================

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health_head():
    return Response(status_code=200)

# =====================================================
# NORMALIZE FUNCTION
# =====================================================

def normalize_planet(p):
    return {
        "name": p.get("name") or p.get("pl_name") or "Unknown",
        "host_star": p.get("host_star") or p.get("hostname") or "Unknown",
        "radius_earth": p.get("radius_earth") or p.get("pl_rade"),
        "mass_earth": p.get("mass_earth") or p.get("pl_bmasse"),
        "classification": p.get("classification") or "Unknown"
    }

# =====================================================
# SUGGESTIONS
# =====================================================

@app.get("/suggestions")
def suggestions():
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=20",
            timeout=30
        )
        r.raise_for_status()
        planets = r.json()

        normalized = [normalize_planet(p) for p in planets]

        return normalized[:8]

    except Exception:
        return []

# =====================================================
# SEARCH
# =====================================================

@app.get("/search")
def search(q: str = Query(...)):
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=100",
            timeout=30
        )
        r.raise_for_status()
        planets = r.json()

        normalized = [normalize_planet(p) for p in planets]

        return [
            p for p in normalized
            if q.lower() in p["name"].lower()
        ]

    except Exception:
        return []
