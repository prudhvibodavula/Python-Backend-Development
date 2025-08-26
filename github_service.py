import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set in .env")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def whoami():
    resp = requests.get(f"{GITHUB_API_URL}/user", headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return {"login": data.get("login"), "id": data.get("id")}

def fetch_repo_data(owner: str, repo: str):
    repo_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
    repo_resp = requests.get(repo_url, headers=headers, timeout=20)
    repo_resp.raise_for_status()
    repo_data = repo_resp.json()

    # Branches
    branches_url = f"{repo_url}/branches?per_page=100"
    branches_resp = requests.get(branches_url, headers=headers, timeout=20)
    branches_resp.raise_for_status()
    branches_data = branches_resp.json()
    branch_count = len(branches_data) if isinstance(branches_data, list) else 0

    # Commits
    commits_url = f"{repo_url}/commits?per_page=1"
    commits_resp = requests.get(commits_url, headers=headers, timeout=20)
    commits_resp.raise_for_status()
    commits_data = commits_resp.json()

    commit_count = 0
    last_commit_date = None
    if isinstance(commits_data, list) and len(commits_data) > 0:
        last_commit_date_str = commits_data[0]["commit"]["committer"]["date"]
        last_commit_date = datetime.strptime(last_commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
        if "Link" in commits_resp.headers:
            import re
            m = re.search(r'&page=(\d+)>; rel="last"', commits_resp.headers["Link"])
            commit_count = int(m.group(1)) if m else 1
        else:
            commit_count = len(commits_data)

    return {
        "repo_name": repo_data.get("name"),
        "commit_count": commit_count,
        "branch_count": branch_count,
        "last_commit_date": last_commit_date
    }

def get_all_repo_details():
    url = f"{GITHUB_API_URL}/user/repos?per_page=100"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repos = response.json()

    all_repo_details = []
    for repo in repos:
        owner = repo['owner']['login']
        repo_name = repo['name']

        # Branches
        branches_url = f"{GITHUB_API_URL}/repos/{owner}/{repo_name}/branches?per_page=100"
        branches_resp = requests.get(branches_url, headers=headers)
        branches_resp.raise_for_status()
        branch_count = len(branches_resp.json())

        # Commits
        commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo_name}/commits?per_page=1"
        commits_resp = requests.get(commits_url, headers=headers)
        commits_resp.raise_for_status()
        commits_data = commits_resp.json()
        commit_count = 0
        last_commit_date = None

        if isinstance(commits_data, list) and len(commits_data) > 0:
            last_commit_date_str = commits_data[0]["commit"]["committer"]["date"]
            last_commit_date = datetime.strptime(last_commit_date_str, "%Y-%m-%dT%H:%M:%SZ")
            if "Link" in commits_resp.headers:
                import re
                m = re.search(r'&page=(\d+)>; rel="last"', commits_resp.headers["Link"])
                commit_count = int(m.group(1)) if m else 1
            else:
                commit_count = len(commits_data)

        all_repo_details.append({
            "repo_name": repo_name,
            "commit_count": commit_count,
            "branch_count": branch_count,
            "last_commit_date": last_commit_date
        })

    return all_repo_details
