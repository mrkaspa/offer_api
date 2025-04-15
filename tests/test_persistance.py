import pytest
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.persistance import get_session


def test_database_connection(test_engine):
    """Test database connection and table creation."""
    assert test_engine is not None
    # Verify tables exist using inspect
    inspector = inspect(test_engine)
    print(inspector.get_table_names())
    assert "promotion" in inspector.get_table_names()


def test_session_factory(test_engine):
    """Test session factory creation and management."""
    session_factory = get_session(test_engine)
    session = next(session_factory())
    assert isinstance(session, Session)
    session.close()
