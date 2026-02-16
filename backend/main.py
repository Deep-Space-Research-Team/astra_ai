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

@app.get("/")
def home():
    return FileResponse("backend/static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health_head():
    return Response(status_code=200)

@app.get("/suggestions")
def suggestions():
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=10",
            timeout=30
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@app.get("/search")
def search(q: str = Query(...)):
    try:
        r = requests.get(
            f"{SPACE_DB_URL}/exoplanets?limit=100",
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        return [
            p for p in data
            if q.lower() in (p.get("name") or "").lower()
        ]
    except Exception as e:
        return {"error": str(e)}
