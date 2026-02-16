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

# ======================================================
# ROOT
# ======================================================

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health_head():
    return Response(status_code=200)

# ======================================================
# SUGGESTIONS (INTELLIGENT CURATED)
# ======================================================

@app.get("/suggestions")
def suggestions():
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=50",
            timeout=30
        )
        r.raise_for_status()
        planets = r.json()

        super_earth = [p for p in planets if p.get("classification") == "Super Earth"]
        rocky = [p for p in planets if p.get("classification") == "Rocky"]
        gas = [p for p in planets if p.get("classification") == "Gas Giant"]
        hot = [p for p in planets if p.get("classification") == "Hot Jupiter"]

        curated = (
            super_earth[:2] +
            rocky[:2] +
            gas[:2] +
            hot[:2]
        )

        if len(curated) < 8:
            curated += planets[:8 - len(curated)]

        return curated[:8]

    except Exception as e:
        return {"error": str(e)}

# ======================================================
# SEARCH
# ======================================================

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

    except Exception as e:
        return {"error": str(e)}
