import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

SPACE_DB_URL = os.getenv(
    "SPACE_DB_URL",
    "https://space-object-database.onrender.com"
)

app = FastAPI(title="Astra AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health_head():
    return Response(status_code=200)

# ==========================================
# ROOT
# ==========================================

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

# ==========================================
# SEARCH
# ==========================================

@app.get("/search")
def search(q: str = Query(...)):
    r = requests.get(
        f"{SPACE_DB_URL}/exoplanets?limit=100"
    )
    data = r.json()

    filtered = [
        p for p in data
        if q.lower() in (p.get("name") or "").lower()
    ]

    return filtered

# ==========================================
# SUGGESTIONS
# ==========================================

@app.get("/suggestions")
def suggestions():
    r = requests.get(
        f"{SPACE_DB_URL}/exoplanets?limit=10"
    )
    return r.json()
