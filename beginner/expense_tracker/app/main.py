from fastapi import FastAPI
from .database import Base, engine

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Expense Tracker API running 🚀"}