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
    # Lightweight SQLite column adds for existing DBs
    if settings.database_url.startswith("sqlite"):
        with engine.connect() as conn:
            cols = {row[1] for row in conn.execute(text("PRAGMA table_info(applications)"))}
            if "interview_prep" not in cols:
                conn.execute(text("ALTER TABLE applications ADD COLUMN interview_prep TEXT DEFAULT '{}'"))
            if "analytics_json" not in cols:
                conn.execute(text("ALTER TABLE applications ADD COLUMN analytics_json TEXT DEFAULT '{}'"))
            # Recruiter CRM column adds (Agent 2.0)
            try:
                crm_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(recruiter_contacts)"))}
            except Exception:  # noqa: BLE001
                crm_cols = set()
            if crm_cols:
                alters = {
                    "role": "ALTER TABLE recruiter_contacts ADD COLUMN role TEXT DEFAULT ''",
                    "application_date": "ALTER TABLE recruiter_contacts ADD COLUMN application_date DATE",
                    "status": "ALTER TABLE recruiter_contacts ADD COLUMN status TEXT DEFAULT 'active'",
                    "referral_source": "ALTER TABLE recruiter_contacts ADD COLUMN referral_source TEXT DEFAULT ''",
                }
                for col, sql in alters.items():
                    if col not in crm_cols:
                        conn.execute(text(sql))
            conn.commit()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
