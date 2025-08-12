from fastapi import FastAPI
from sqlalchemy.orm import Session
import database

app = FastAPI()

@app.get("/")
def hello_world():
    return {"Hello World!!!"}