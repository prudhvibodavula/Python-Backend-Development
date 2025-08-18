from fastapi import FastAPI,HTTPException, Depends
from sqlalchemy.orm import Session
import database, models, schemas, crud

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