from sqlalchemy.orm import Session
from app.models.user_rates import UserRate
from app.schemas.user_rate import UserRateCSVSchema

def create_user_rate(db: Session, user_rate: UserRateCSVSchema):
    db_user_rate = UserRate(
        user_email=user_rate.user_email,
        origin=user_rate.origin,
        destination=user_rate.destination,
        effective_date=user_rate.effective_date,
        expiry_date=user_rate.expiry_date,
        price=user_rate.price,
        annual_volume=user_rate.annual_volume
    )
    try:
        db.add(db_user_rate)
        db.commit()
        db.refresh(db_user_rate)
    except Exception:
        db.rollback()
        raise
    return db_user_rate

def get_distinct_user_rates(db: Session):
    return db.query(
        UserRate.expiry_date,
        UserRate.effective_date,
        UserRate.origin,
        UserRate.destination,
        UserRate.price,
        UserRate.annual_volume).distinct().all()

def get_user_rates(db: Session, expiry_date, effective_date, origin, destination):
    return db.query(UserRate).filter(
        UserRate.effective_date == effective_date,
        UserRate.expiry_date == expiry_date,
        UserRate.origin == origin,
        UserRate.destination == destination
    ).all()
