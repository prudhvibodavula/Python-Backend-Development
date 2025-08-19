import os
import requests
from dotenv import load_dotenv

load_dotenv()  

GITHUB_API = "https://api.github.com"

def _auth_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set in .env")
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

def whoami():
    """
    Simple call to verify the token works.
    Returns your GitHub login and id.
    """
    resp = requests.get(f"{GITHUB_API}/user", headers=_auth_headers(), timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return {"login": data.get("login"), "id": data.get("id")}
