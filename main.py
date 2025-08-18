from fastapi import FastAPI, Depends
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
