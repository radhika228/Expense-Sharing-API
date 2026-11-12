from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, groups, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Sharing API",
    description="Backend service for managing groups, shared expenses, and balances.",
    version="2.0.0",
)

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(expenses.router)


@app.get("/")
def home():
    return {"message": "Welcome to Expense Sharing API"}
