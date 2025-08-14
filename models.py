from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base

class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String, nullable=False)
    commit_count = Column(Integer)
    branch_count = Column(Integer)
    last_commit_date = Column(TIMESTAMP)
