from sqlalchemy import DECIMAL, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AggregatedMarketRate(Base):
    __tablename__ = "aggregated_market_rates"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    origin = Column(String)
    destination = Column(String)
    min_price = Column(DECIMAL)
    percentile_10_price = Column(DECIMAL)
    median_price = Column(DECIMAL)
    percentile_90_price = Column(DECIMAL)
    max_price = Column(DECIMAL)