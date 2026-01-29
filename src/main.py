from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.config import settings
from src.database import database
from src.routers import users, wallets, transactions, statistics


app = FastAPI(
    title="Bitcoin Wallet API",
    description="A RESTful API for managing Bitcoin wallets",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event() -> None:
    database.create_tables()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    pass


@app.get("/", tags=["Health"])
async def root() -> JSONResponse:
    return JSONResponse(
        content={"message": "Bitcoin Wallet API", "status": "running"}
    )


app.include_router(users.router)
app.include_router(wallets.router)
app.include_router(transactions.router)
app.include_router(statistics.router)

