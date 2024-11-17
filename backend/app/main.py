from fastapi import FastAPI
from app.api import upload_csv_api
from app.api import market_aggregated_rates_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(upload_csv_api.router, prefix="/upload", tags=["upload"])

app.include_router(market_aggregated_rates_api.router, prefix="/market", tags=["market"])