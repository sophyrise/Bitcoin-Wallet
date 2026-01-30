from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.database import database
from src.routers import statistics, transactions, users, wallets

app = FastAPI(
    title="Bitcoin Wallet API",
    description="A RESTful API for managing Bitcoin wallets",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event() -> None:
    database.create_tables()
    print("Swagger docs: http://127.0.0.1:8000/docs")


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

