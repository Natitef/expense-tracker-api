from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Expense Tracker API",
    description="A REST API for tracking personal expenses",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}