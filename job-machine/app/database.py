from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    from app import models  # noqa: F401
    from sqlalchemy import text

    Base.metadata.create_all(bind=engine)
    # Lightweight SQLite column add for interview_prep on existing DBs
    if settings.database_url.startswith("sqlite"):
        with engine.connect() as conn:
            cols = {row[1] for row in conn.execute(text("PRAGMA table_info(applications)"))}
            if "interview_prep" not in cols:
                conn.execute(text("ALTER TABLE applications ADD COLUMN interview_prep TEXT DEFAULT '{}'"))
                conn.commit()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
