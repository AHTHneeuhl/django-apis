from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Social Media API")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}