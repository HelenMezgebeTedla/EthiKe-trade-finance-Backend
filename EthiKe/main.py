import os

from dotenv import load_dotenv

load_dotenv()

import app.models
from app.core.rate_limit import limiter
from database import Base, engine
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

Base.metadata.create_all(bind=engine)

from app.routers import (
    auth,
    cash_snapshot,
    credit,
    prediction,
    price_index,
    product,
    purchase,
    sale,
    trader,
    transaction,
    user,
)

app = FastAPI(title="Trader Financial Resilience API", version="2")


allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Strict-Transport-Security"] = (
        "max-age=63072000; includeSubDomains"
    )
    return response


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(trader.router)
app.include_router(transaction.router)
app.include_router(product.router)
app.include_router(purchase.router)
app.include_router(sale.router)
app.include_router(credit.router)
app.include_router(price_index.router)
app.include_router(cash_snapshot.router)
app.include_router(prediction.router)


@app.get("/")
def root():
    return {"message": "Trader Financial Resilience API is running."}
