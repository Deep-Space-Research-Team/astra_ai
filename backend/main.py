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

# ==========================================
# ROOT
# ==========================================

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health_head():
    return Response(status_code=200)

# ==========================================
# SUGGESTIONS (GUARANTEED NON-EMPTY)
# ==========================================

@app.get("/suggestions")
def suggestions():
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=20",
            timeout=30
        )
        r.raise_for_status()
        planets = r.json()

        if not isinstance(planets, list) or not planets:
            return []

        # Group by classification
        groups = {}
        for p in planets:
            cls = p.get("classification", "Unknown")
            groups.setdefault(cls, []).append(p)

        curated = []

        # Pick 1 from each type
        for cls in groups:
            curated.append(groups[cls][0])

        # Ensure at least 6 suggestions
        if len(curated) < 6:
            curated = planets[:6]

        return curated[:8]

    except Exception:
        return []

# ==========================================
# SEARCH
# ==========================================

@app.get("/search")
def search(q: str = Query(...)):
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=100",
            timeout=30
        )
        r.raise_for_status()
        planets = r.json()

        filtered = [
            p for p in planets
            if q.lower() in (p.get("name") or "").lower()
        ]

        return filtered

    except Exception:
        return []
