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

def update_repo(db: Session, repo_id: int, repo: schemas.RepoUpdate):
    db_repo = db.query(models.Repo).filter(models.Repo.id == repo_id).first()
    if not db_repo:
        return None

    update_data = repo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_repo, key, value)

    db.commit()
    db.refresh(db_repo)
    return db_repo

def delete_repo(db: Session, repo_id: int):
    db_repo = db.query(models.Repo).filter(models.Repo.id == repo_id).first()
    if not db_repo:
        return None  
    db.delete(db_repo)
    db.commit()
    return db_repo