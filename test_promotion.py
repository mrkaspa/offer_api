import pytest
from datetime import datetime, date
from promotion import Promotion, CreatePromotionModel, PromotionType, generate_slug
from persistance import Base
from tests.factories.promotion_factory import PromotionFactory


@pytest.fixture
def test_promotion_data():
    """Sample promotion data for testing."""
    return {
        "name": "Test Promotion",
        "description": "Test Description",
        "promotion_type": PromotionType.DISCOUNT,
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31),
        "is_active": True,
    }


def test_generate_slug():
    """Test slug generation function."""
    # Test without ID
    assert generate_slug("Test Promotion") == "test-promotion"

    # Test with ID
    assert generate_slug("Test Promotion", 1) == "test-promotion-1"

    # Test with special characters
    assert generate_slug("Test & Promotion!") == "test-promotion"

    # Test with multiple spaces
    assert generate_slug("Test & Promotion") == "test-promotion"


def test_promotion_model_creation(test_promotion_data):
    """Test PromotionModel creation and validation."""
    # Test basic creation
    promotion = CreatePromotionModel(**test_promotion_data)
    assert promotion.name == "Test Promotion"
    assert promotion.description == "Test Description"
    assert promotion.promotion_type == PromotionType.DISCOUNT
    assert promotion.is_active is True


def test_create_promotion(test_session):
    # Create a promotion
    promotion = Promotion(
        name="Test Promotion",
        description="Test Description",
        promotion_type=PromotionType.DISCOUNT,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        is_active=True
    )

    # Add to session and commit
    test_session.add(promotion)
    test_session.commit()

    # Refresh to get the generated ID and slug
    test_session.refresh(promotion)

    # Assert the promotion was created correctly
    assert promotion.id is not None
    assert promotion.name == "Test Promotion"
    assert promotion.slug == f"test-promotion-{promotion.id}"
    assert promotion.created_at is not None
    assert promotion.updated_at is not None


def test_promotion_crud_operations(test_session):
    # Create a promotion using the factory
    promotion = PromotionFactory()
    test_session.add(promotion)
    test_session.commit()
    test_session.refresh(promotion)

    # Test reading
    assert promotion.id is not None
    assert promotion.name is not None
    assert promotion.slug is not None

    # Test updating
    original_name = promotion.name
    promotion.name = "Updated Name"
    test_session.commit()
    test_session.refresh(promotion)
    assert promotion.name == "Updated Name"
    assert promotion.name != original_name

    # Test deleting
    promotion_id = promotion.id
    test_session.delete(promotion)
    test_session.commit()
    assert test_session.query(Promotion).filter(Promotion.id == promotion_id).first() is None


def test_promotion_unique_slug(test_session, test_promotion_data):
    """Test that slugs are unique."""
    # Create first promotion
    promotion1 = Promotion(**test_promotion_data)
    test_session.add(promotion1)
    test_session.commit()

    # Create second promotion with same name
    promotion2 = Promotion(**test_promotion_data)
    test_session.add(promotion2)
    test_session.commit()
    test_session.refresh(promotion2)

    # Verify slugs are different
    assert promotion1.slug != promotion2.slug
    assert promotion1.slug == f"test-promotion-{promotion1.id}"
    assert promotion2.slug == f"test-promotion-{promotion2.id}"
