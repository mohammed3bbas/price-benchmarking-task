from fastapi import FastAPI
from app.api import upload_csv_api
from app.api import market_aggregated_rates_api

app = FastAPI()

app.include_router(upload_csv_api.router, prefix="/upload", tags=["upload"])

app.include_router(market_aggregated_rates_api.router, prefix="/market", tags=["market"])