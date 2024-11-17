import csv
from io import StringIO
from datetime import datetime
from app.schemas.user_rate import UserRateCSVSchema
from typing import List

def parse_csv(file_contents: bytes) -> List[UserRateCSVSchema]:
    """
    Parse the CSV file contents and validate the data.
    """
    decoded = file_contents.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    valid_data = []
    for row in reader:
        # Validate with Pydantic schema
        try:
            print(row)
            validated_row = UserRateCSVSchema(
                # user_email=row['user_email'],
                origin=row['origin'],
                destination=row['destination'],
                effective_date=datetime.strptime(row['effective_date'], '%Y/%m/%d').date(),
                expiry_date=datetime.strptime(row['expiry_date'], '%Y/%m/%d').date(),
                price=float(row['price']),
                annual_volume=float(row['annual_volume'])
            )
            print(validated_row)
            valid_data.append(validated_row)
        except ValueError as e:
            raise ValueError(f"Invalid data in row: {row}, error: {e}")
    return valid_data
