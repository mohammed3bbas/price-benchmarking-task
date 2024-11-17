from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserRate(Base):
    __tablename__ = "users_rates"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    origin = Column(String)
    destination = Column(String)
    effective_date = Column(Date)
    expiry_date = Column(Date)
    price = Column(Numeric(10, 2))
    annual_volume = Column(Numeric(10, 2))