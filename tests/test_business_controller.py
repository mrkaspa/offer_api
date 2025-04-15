import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.persistance import Base
from app.server import app
from app.dependencies import engine
from tests.factories.business_factory import BusinessFactory


@pytest.fixture(scope="function")
def client(test_engine):
    # Override the dependency to use our test session
    def override_get_db():
        try:
            yield test_engine

        finally:
            pass

    app.dependency_overrides[engine] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_get_business(client, test_session):
    business = BusinessFactory()
    test_session.add(business)
    test_session.commit()

    response = client.get(f"/businesses/{business.id}")

    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["id"] == business.id
    assert data["name"] == business.name
    assert data["description"] == business.description


def test_get_businesses(client, test_session):
    businesses = BusinessFactory.create_batch(3)
    test_session.add_all(businesses)
    test_session.commit()

    response = client.get("/businesses/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_create_business(client):
    response = client.post(
        "/businesses/",
        json={
            "name": "Test Business",
            "description": "Test Description",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test Business"
    assert response.json()["description"] == "Test Description"


def test_update_business(client, test_session):
    business = BusinessFactory()
    test_session.add(business)
    test_session.commit()

    response = client.put(
        f"/businesses/{business.id}",
        json={
            "name": "New Name",
        },
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_business(client, test_session):
    business = BusinessFactory()
    test_session.add(business)
    test_session.commit()

    response = client.delete(f"/businesses/{business.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Business deleted successfully"
