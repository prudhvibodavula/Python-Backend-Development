from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database, models
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

@app.post("/repos/")
def create_repo(repo_name: str, commit_count: int, branch_count: int, last_commit_date: str, db: Session = Depends(get_db)):
    repo = models.Repo(
        repo_name=repo_name,
        commit_count=commit_count,
        branch_count=branch_count,
        last_commit_date=last_commit_date
    )
    db.add(repo)
    db.commit()
    db.refresh(repo)
    return repo


@app.get("/repos/")
def get_repos(db: Session = Depends(get_db)):
    repos = db.query(models.Repo).all()
    return repos
