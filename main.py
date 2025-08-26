from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import database, models, schemas, crud, github_service

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def hello_world():
    return {"message": "Hello World!!!"}

@app.post("/repos/", response_model=schemas.RepoResponse)
def create_repo(repo: schemas.RepoCreate, db: Session = Depends(get_db)):
    return crud.create_repo(db, repo)

@app.get("/repos/", response_model=list[schemas.RepoResponse])
def get_repos(db: Session = Depends(get_db)):
    return crud.get_repos(db)

@app.patch("/repos/{repo_id}", response_model=schemas.RepoResponse)
def update_repo_endpoint(repo_id: int, repo: schemas.RepoUpdate, db: Session = Depends(get_db)):
    db_repo = crud.update_repo(db, repo_id, repo)
    if not db_repo:
        raise HTTPException(status_code=404, detail="Repo not found")
    return db_repo

@app.delete("/repos/{repo_id}", response_model=schemas.RepoResponse)
def delete_repo_endpoint(repo_id: int, db: Session = Depends(get_db)):
    db_repo = crud.delete_repo(db, repo_id)
    if not db_repo:
        raise HTTPException(status_code=404, detail="Repo not found")
    return db_repo

@app.get("/github/me")
def github_me():
    try:
        return github_service.whoami()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/github/repos/{owner}/{repo}")
def get_repo(owner: str, repo: str):
    try:
        return github_service.fetch_repo_data(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/github/fetch-repos-to-db")
def fetch_and_store_repos(db: Session = Depends(get_db)):
    try:
        repos_data = github_service.get_all_repo_details()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repos: {e}")

    saved_repos = []

    for repo in repos_data:
        # Ensure last_commit_date is datetime or None
        last_commit_date = repo.get("last_commit_date")
        repo["last_commit_date"] = last_commit_date

        # Check for existing repo
        existing_repo = db.query(models.Repo).filter(models.Repo.repo_name == repo["repo_name"]).first()
        if existing_repo:
            saved_repos.append(existing_repo)
            continue

        # Insert new repo
        repo_schema = schemas.RepoCreate(**repo)
        saved_repo = crud.create_repo(db, repo_schema)
        saved_repos.append(saved_repo)

    return {"saved_count": len(saved_repos), "repos": saved_repos}
