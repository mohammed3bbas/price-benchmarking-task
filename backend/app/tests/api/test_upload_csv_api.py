import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.schemas.user_rate import UserRateCSVSchema
from app.cruds.user_rate import create_user_rate
from app.utils.file_uplode import parse_csv

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def valid_csv_data():
    return b"origin,destination,effective_date,expiry_date,price,annual_volume\n" \
           b"USA,Canada,2024-01-01,2025-01-01,100.0,5000\n" \
           b"Canada,USA,2024-02-01,2025-02-01,150.0,6000"

@pytest.fixture
def mock_upload_file(valid_csv_data):
    mock_file = MagicMock()
    mock_file.read.return_value = valid_csv_data
    return mock_file

def test_upload_csv(client, mock_db_session, mock_upload_file):
    mock_user_rate = UserRateCSVSchema(
        origin="USA",
        destination="Canada",
        effective_date="2024-01-01",
        expiry_date="2025-01-01",
        price=100.0,
        annual_volume=5000
    )

    response = client.post("/upload/csv/", files={"file": ("test.csv", mock_upload_file, "text/csv")})

    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully and data saved."}
    create_user_rate.assert_called_once_with(mock_db_session, mock_user_rate)

def test_upload_csv_invalid_data(client, mock_db_session):
    invalid_csv_data = b"origin,destination,effective_date,expiry_date,price,annual_volume\n" \
                       b"USA,Canada,invalid_date,2025/01/01,100.0,5000"
    
    mock_upload_file = MagicMock()
    mock_upload_file.read.return_value = invalid_csv_data

    response = client.post("/upload/csv/", files={"file": ("test.csv", mock_upload_file, "text/csv")})

    assert response.status_code == 400
    assert "Error in processing the CSV file" in response.json()["detail"]
