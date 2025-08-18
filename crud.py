from sqlalchemy.orm import Session
import models, schemas

def create_repo(db: Session, repo: schemas.RepoCreate):
    db_repo = models.Repo(
        repo_name=repo.repo_name,
        commit_count=repo.commit_count,
        branch_count=repo.branch_count,
        last_commit_date=repo.last_commit_date
    )
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo

def get_repos(db: Session):
    return db.query(models.Repo).all()
