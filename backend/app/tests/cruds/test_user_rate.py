import pytest
from unittest.mock import MagicMock
from app.models.user_rates import UserRate
from app.schemas.user_rate import UserRateCSVSchema
from app.cruds.user_rate import create_user_rate, get_distinct_user_rates, get_user_rates

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def mock_user_rate():
    return UserRateCSVSchema(
        user_email="test@example.com",
        origin="NYC",
        destination="LA",
        effective_date="2024-01-01",
        expiry_date="2024-12-31",
        price=100.5,
        annual_volume=1000
    )

def test_create_user_rate(mock_db_session, mock_user_rate):
    db_user_rate = create_user_rate(mock_db_session, mock_user_rate)
    assert db_user_rate.user_email == mock_user_rate.user_email
    assert db_user_rate.origin == mock_user_rate.origin
    assert db_user_rate.destination == mock_user_rate.destination
    assert db_user_rate.effective_date == mock_user_rate.effective_date
    assert db_user_rate.expiry_date == mock_user_rate.expiry_date
    assert db_user_rate.price == mock_user_rate.price
    assert db_user_rate.annual_volume == mock_user_rate.annual_volume
    mock_db_session.add.assert_called_once_with(db_user_rate)
    mock_db_session.commit.assert_called_once()

def test_get_distinct_user_rates(mock_db_session):
    mock_db_session.query().distinct().all.return_value = [
        ("2024-12-31", "2024-01-01", "NYC", "LA", 100.5, 1000)
    ]
    distinct_rates = get_distinct_user_rates(mock_db_session)
    assert len(distinct_rates) == 1
    assert distinct_rates[0] == ("2024-12-31", "2024-01-01", "NYC", "LA", 100.5, 1000)

def test_get_user_rates(mock_db_session):
    mock_db_session.query().filter().all.return_value = [
        UserRate(
            user_email="test@example.com",
            origin="NYC",
            destination="LA",
            effective_date="2024-01-01",
            expiry_date="2024-12-31",
            price=100.5,
            annual_volume=1000
        )
    ]
    user_rates = get_user_rates(mock_db_session, "2024-12-31", "2024-01-01", "NYC", "LA")
    assert len(user_rates) == 1
    assert user_rates[0].user_email == "test@example.com"
    assert user_rates[0].origin == "NYC"
    assert user_rates[0].destination == "LA"
    assert user_rates[0].effective_date == "2024-01-01"
    assert user_rates[0].expiry_date == "2024-12-31"
    assert user_rates[0].price == 100.5
    assert user_rates[0].annual_volume == 1000
