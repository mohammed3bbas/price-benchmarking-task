import pytest
from datetime import datetime
from app.schemas.user_rate import UserRateCSVSchema
from app.utils.file_uplode import parse_csv  

@pytest.fixture
def valid_csv_data():
    return b"origin,destination,effective_date,expiry_date,price,annual_volume\n" \
           b"USA,Canada,2024/01/01,2025/01/01,100.0,5000\n" \
           b"Canada,USA,2024/02/01,2025/02/01,150.0,6000"

@pytest.fixture
def invalid_csv_data():
    return b"origin,destination,effective_date,expiry_date,price,annual_volume\n" \
           b"USA,Canada,2024/01/01,2025/01/01,100.0,5000\n" \
           b"Canada,USA,invalid_date,2025/02/01,150.0,6000"  

def test_parse_csv_valid(valid_csv_data):
    parsed_data = parse_csv(valid_csv_data)
    
    assert len(parsed_data) == 2

    assert parsed_data[0].origin == "USA"
    assert parsed_data[0].destination == "Canada"
    assert parsed_data[0].effective_date == datetime(2024, 1, 1).date()
    assert parsed_data[0].expiry_date == datetime(2025, 1, 1).date()
    assert parsed_data[0].price == 100.0
    assert parsed_data[0].annual_volume == 5000.0

    assert parsed_data[1].origin == "Canada"
    assert parsed_data[1].destination == "USA"
    assert parsed_data[1].effective_date == datetime(2024, 2, 1).date()
    assert parsed_data[1].expiry_date == datetime(2025, 2, 1).date()
    assert parsed_data[1].price == 150.0
    assert parsed_data[1].annual_volume == 6000.0

def test_parse_csv_invalid_date(invalid_csv_data):
    with pytest.raises(ValueError):
        parse_csv(invalid_csv_data)
    
def test_parse_csv_missing_column():
    invalid_data = b"origin,destination,effective_date,expiry_date,price\n" \
                   b"USA,Canada,2024/01/01,2025/01/01,100.0"  
    
    with pytest.raises(KeyError):
        parse_csv(invalid_data)

def test_parse_csv_invalid_price():
    invalid_data = b"origin,destination,effective_date,expiry_date,price,annual_volume\n" \
                   b"USA,Canada,2024/01/01,2025/01/01,invalid_price,5000"
    
    with pytest.raises(ValueError):
        parse_csv(invalid_data)
