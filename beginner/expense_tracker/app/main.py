from fastapi import FastAPI
from .database import Base, engine
from .routes import transactions, reports, categories, auth

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

app.include_router(transactions.router)
app.include_router(reports.router)
app.include_router(categories.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API running 🚀"}