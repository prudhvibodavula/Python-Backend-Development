import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"

def _auth_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set in .env")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

def whoami():
    """
    Optional: Verify the GitHub token works.
    Returns your GitHub login and id.
    """
    resp = requests.get(f"{GITHUB_API}/user", headers=_auth_headers(), timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return {"login": data.get("login"), "id": data.get("id")}

def fetch_repo_data(owner: str, repo: str):
    """
    Fetch repository information including:
    - repo_name
    - last_commit_date
    - commit_count
    - branch_count
    """
    # Repo details
    repo_url = f"{GITHUB_API}/repos/{owner}/{repo}"
    repo_resp = requests.get(repo_url, headers=_auth_headers(), timeout=20)
    repo_resp.raise_for_status()
    repo_data = repo_resp.json()

    # Commits
    commits_url = f"{repo_url}/commits"
    commits_resp = requests.get(commits_url, headers=_auth_headers(), timeout=20)
    commits_resp.raise_for_status()
    commits_data = commits_resp.json()
    commit_count = len(commits_data) if isinstance(commits_data, list) else 0
    last_commit_date = commits_data[0]["commit"]["committer"]["date"] if commit_count > 0 else None

    # Branches
    branches_url = f"{repo_url}/branches"
    branches_resp = requests.get(branches_url, headers=_auth_headers(), timeout=20)
    branches_resp.raise_for_status()
    branches_data = branches_resp.json()
    branch_count = len(branches_data) if isinstance(branches_data, list) else 0

    return {
        "repo_name": repo_data.get("name"),
        "last_commit_date": last_commit_date,
        "commit_count": commit_count,
        "branch_count": branch_count
    }
