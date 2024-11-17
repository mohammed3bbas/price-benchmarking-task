from pydantic import BaseModel, EmailStr, Field, ValidationInfo, FieldValidationInfo,field_validator
from typing import Optional
from datetime import date

class UserRateCSVSchema(BaseModel):
    user_email: Optional[EmailStr] = None
    origin: str
    destination: str
    effective_date: date
    expiry_date: date
    price: float = Field(..., gt=0)
    annual_volume: float = Field(..., gt=0)

    @field_validator("expiry_date")
    def check_expiry_date(cls, expiry_date, info: FieldValidationInfo):
        if "effective_date" in info.data and expiry_date <= info.data["effective_date"]:
            raise ValueError("expiry_date must be after effective_date")
        return expiry_date

    @field_validator("origin", "destination")
    def check_no_special_characters(cls, value):
        if not value.isalnum():
            raise ValueError("Origin and destination must only contain alphanumeric characters")
        return value
