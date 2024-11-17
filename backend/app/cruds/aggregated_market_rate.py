from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.aggregated_market_rate import AggregatedMarketRate
from app.schemas.aggregated_market_rate import AggregatedMarketRateSchema

def get_aggregated_rate(db: Session, expiry_date, effective_date, origin, destination):
    return db.query(AggregatedMarketRate).filter(
        AggregatedMarketRate.date < expiry_date,
        AggregatedMarketRate.date >= effective_date,
        AggregatedMarketRate.origin == origin,
        AggregatedMarketRate.destination == destination
    ).all()

def create_aggregated_rate(db: Session, data):
    new_rate = AggregatedMarketRate(**data)
    db.add(new_rate)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    return new_rate
