import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.persistance import Base
from app.server import app
from app.dependencies import engine
from app.domain.models import Promotion
from tests.factories.promotion_factory import PromotionFactory


@pytest.fixture(scope="function")
def client(test_engine):
    # Override the dependency to use our test session
    def override_get_db():
        try:
            yield test_engine
        finally:
            pass

    app.dependency_overrides[engine] = override_get_db

    # Create a test client
    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()


def test_get_promotions(client, test_session):
    # Create some test promotions using the factory
    promotions = PromotionFactory.create_batch(3)
    test_session.add_all(promotions)
    test_session.commit()

    response = client.get("/promotions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Verify the promotions were created correctly
    for promotion in promotions:
        assert any(p["id"] == promotion.id for p in data)
        assert any(p["name"] == promotion.name for p in data)
        assert any(p["slug"] == promotion.slug for p in data)


def test_get_promotion_by_slug(client, test_session):
    # Create a test promotion
    promotion = PromotionFactory()
    test_session.add(promotion)
    test_session.commit()

    # Test getting the promotion by slug
    response = client.get(f"/promotions/{promotion.slug}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == promotion.id
    assert data["name"] == promotion.name
    assert data["slug"] == promotion.slug


def test_create_promotion(client):
    response = client.post(
        "/promotions/",
        json={
            "name": "Test Promotion",
            "description": "Test Description",
            "promotion_type": "discount",
            "start_date": "2024-06-01",
            "end_date": "2024-08-31",
            "is_active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Promotion"
    assert data["description"] == "Test Description"
    assert data["promotion_type"] == "discount"
    assert data["slug"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_update_promotion(client, test_session):
    # Create a test promotion
    promotion = PromotionFactory()
    test_session.add(promotion)
    test_session.commit()

    # Test updating the promotion
    response = client.put(
        f"/promotions/{promotion.slug}",
        json={
            "name": "Updated Promotion",
            "description": "Updated Description",
            "promotion_type": "discount",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Promotion"
    assert data["description"] == "Updated Description"
    assert data["promotion_type"] == "discount"


def test_delete_promotion(client, test_session):
    # Create a test promotion
    promotion = PromotionFactory()
    test_session.add(promotion)
    test_session.commit()

    # Test deleting the promotion
    response = client.delete(f"/promotions/{promotion.slug}")
    assert response.status_code == 200
    assert response.json() == {"message": "Promotion deleted successfully"}

    # Verify the promotion is deleted
    assert (
        test_session.query(Promotion).filter(Promotion.id == promotion.id).first()
        is None
    )
