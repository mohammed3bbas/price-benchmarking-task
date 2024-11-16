from sqlalchemy.orm import Session
from app.models.user_rates import UserRate
from app.schemas.user_rate import UserRateCSV

def create_user_rate(db: Session, user_rate: UserRateCSV):
    """
    Store the user rate data in the database.
    """
    db_user_rate = UserRate(
        user_email=user_rate.user_email,
        origin=user_rate.origin,
        destination=user_rate.destination,
        effective_date=user_rate.effective_date,
        expiry_date=user_rate.expiry_date,
        price=user_rate.price,
        annual_volume=user_rate.annual_volume
    )
    db.add(db_user_rate)
    db.commit()
    db.refresh(db_user_rate)
    return db_user_rate
