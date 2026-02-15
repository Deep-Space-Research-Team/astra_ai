import requests
from backend.config import NASA_API_BASE

def fetch_exoplanets(limit=200):
    r = requests.get(
        f"{NASA_API_BASE}/exoplanets",
        params={"limit": limit},
        timeout=30
    )
    r.raise_for_status()
    return r.json()
