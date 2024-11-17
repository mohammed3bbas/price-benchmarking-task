from pydantic import BaseModel
from datetime import date

class AggregatedMarketRateSchema(BaseModel):
    date: date
    origin: str
    destination: str
    min_price: float
    percentile_10_price: float
    median_price: float
    percentile_90_price: float
    max_price: float