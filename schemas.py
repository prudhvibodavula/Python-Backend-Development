from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class RepoBase(BaseModel):
    repo_name: str
    commit_count: int
    branch_count: int
    last_commit_date: Optional[datetime] = None

class RepoCreate(RepoBase):
    pass

class RepoResponse(RepoBase):
    id: int
    class Config:
        orm_mode = True

class RepoUpdate(BaseModel):
    repo_name: Optional[str] = None
    commit_count: Optional[int] = None
    branch_count: Optional[int] = None
    last_commit_date: Optional[datetime] = None