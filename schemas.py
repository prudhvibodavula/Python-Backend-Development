from pydantic import BaseModel
from datetime import datetime

class RepoBase(BaseModel):
    repo_name: str
    commit_count: int
    branch_count: int
    last_commit_date: datetime

class RepoCreate(RepoBase):
    pass  

class RepoResponse(RepoBase):
    id: int

    class Config:
        orm_mode = True  
