from datetime import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column

Base = declarative_base()


class TimestampMixin:
    """Mixin class that adds created_at and updated_at columns and event listeners."""

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )


def connect_to_db():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    return engine


def create_db_and_tables(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    def session_factory():
        with Session(engine) as session:
            yield session

    return session_factory
