import pytest
from business import Business, CreateBusinessModel, Location, CreateLocationModel


@pytest.fixture
def test_business_data():
    return {
        "name": "Test Business",
        "description": "Test Description",
    }


@pytest.fixture
def test_location_data(test_session):
    return {
        "name": "Test Location",
        "description": "Test Description",
        "address": "Test Address",
        "city": "Test City",
        "state": "Test State",
        "zip_code": "Test Zip Code",
        "country": "Test Country",
        "latitude": 1.0,
        "longitude": 1.0,
    }


@pytest.fixture
def test_business_persisted(test_session, test_business_data):
    business_model = CreateBusinessModel(**test_business_data)
    business = Business(**business_model.model_dump())
    test_session.add(business)
    test_session.commit()
    test_session.refresh(business)
    return business


def test_business_model_creation(test_business_data):
    business_model = CreateBusinessModel(**test_business_data)
    assert business_model.name == "Test Business"
    assert business_model.description == "Test Description"


def test_business_crud_operations(test_session, test_business_data):
    business_model = CreateBusinessModel(**test_business_data)
    business = Business(**business_model.model_dump())
    print("Adding business")
    test_session.add(business)
    test_session.commit()
    test_session.refresh(business)

    assert business.id is not None
    assert business.name == "Test Business"
    assert business.description == "Test Description"

    # Read
    saved_business = (
        test_session.query(Business).filter_by(name="Test Business").first()
    )
    assert saved_business is not None
    assert saved_business.name == "Test Business"
    assert saved_business.description == "Test Description"

    # Update
    saved_business.description = "Updated Description"
    test_session.commit()
    test_session.refresh(saved_business)
    assert saved_business.description == "Updated Description"

    # Delete
    test_session.delete(saved_business)
    test_session.commit()
    assert test_session.query(Business).filter_by(name="Test Business").first() is None


def test_location_model_creation(test_location_data, test_business_persisted):
    test_location_data["business_id"] = test_business_persisted.id
    location_model = CreateLocationModel(**test_location_data)
    assert location_model.name == "Test Location"
    assert location_model.description == "Test Description"
    assert location_model.address == "Test Address"
    assert location_model.city == "Test City"
    assert location_model.state == "Test State"
    assert location_model.business_id is not None


def test_location_crud_operations(
    test_session, test_location_data, test_business_persisted
):
    test_location_data["business_id"] = test_business_persisted.id
    location_model = CreateLocationModel(**test_location_data)
    location = Location(**location_model.model_dump())
    test_session.add(location)
    test_session.commit()
    test_session.refresh(location)

    assert location.id is not None
    assert location.name == "Test Location"
    assert location.description == "Test Description"
    assert location.address == "Test Address"
    assert location.city == "Test City"
    assert location.state == "Test State"

    # Read
    saved_location = (
        test_session.query(Location).filter_by(name="Test Location").first()
    )
    assert saved_location is not None
    assert saved_location.name == "Test Location"
    assert saved_location.description == "Test Description"
    assert saved_location.business_id == test_business_persisted.id
    assert saved_location.business is not None

    # Update
    saved_location.description = "Updated Description"
    test_session.commit()
    test_session.refresh(saved_location)
    assert saved_location.description == "Updated Description"

    # Delete
    test_session.delete(saved_location)
    test_session.commit()
    assert test_session.query(Location).filter_by(name="Test Location").first() is None
