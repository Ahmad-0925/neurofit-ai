from fastapi import FastAPI
from core.database import Base, engine
from db import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "NeuroFit AI is running!"}