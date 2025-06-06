import pytest
from sqlalchemy.orm import Session
from app.persistance import connect_to_db, create_db_and_tables, Base


@pytest.fixture(autouse=True)
def cleanup_database():
    """Clean up the database after each test."""
    yield
    # This will run after each test
    engine = connect_to_db()
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = connect_to_db()
    # Create tables
    create_db_and_tables(engine)
    yield engine
    # Note: We don't need to drop tables here anymore as it's handled by cleanup_database


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    session = Session(test_engine)
    yield session
    session.rollback()  # Rollback any uncommitted changes
    session.close()
