from fastapi import FastAPI
from core.database import Base, engine
from db import models
from api.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "NeuroFit AI is running!"}