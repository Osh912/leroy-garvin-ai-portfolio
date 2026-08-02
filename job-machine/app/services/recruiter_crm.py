from __future__ import annotations

"""Recruiter CRM — local tracking only. Never sends email automatically."""

from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models import Application, RecruiterContact


def list_contacts(db: Session) -> list[dict[str, Any]]:
    rows = db.query(RecruiterContact).order_by(RecruiterContact.updated_at.desc()).all()
    return [_out(r) for r in rows]


def get_contact(db: Session, contact_id: int) -> dict[str, Any] | None:
    row = db.get(RecruiterContact, contact_id)
    return _out(row) if row else None


def upsert_contact(db: Session, payload: dict[str, Any], contact_id: int | None = None) -> dict[str, Any]:
    if contact_id:
        row = db.get(RecruiterContact, contact_id)
        if not row:
            raise ValueError("Recruiter contact not found")
    else:
        row = RecruiterContact()
        db.add(row)

    for field in (
        "recruiter_name",
        "company",
        "email",
        "phone",
        "linkedin",
        "notes",
        "referral_opportunities",
    ):
        if field in payload and payload[field] is not None:
            setattr(row, field, str(payload[field]).strip())

    if "last_contact" in payload:
        row.last_contact = _parse_date(payload.get("last_contact"))
    if "follow_up_date" in payload:
        row.follow_up_date = _parse_date(payload.get("follow_up_date"))
    if "application_id" in payload:
        row.application_id = payload.get("application_id")

    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return _out(row)


def delete_contact(db: Session, contact_id: int) -> bool:
    row = db.get(RecruiterContact, contact_id)
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True


def import_from_applications(db: Session) -> dict[str, Any]:
    """Create CRM rows from applications that already have recruiter name/email — no invention."""
    apps = db.query(Application).all()
    created = 0
    skipped = 0
    for a in apps:
        name = (a.recruiter_name or "").strip()
        email = (a.recruiter_email or "").strip()
        if not name and not email:
            skipped += 1
            continue
        exists = (
            db.query(RecruiterContact)
            .filter(
                RecruiterContact.company == a.company,
                RecruiterContact.recruiter_name == name,
                RecruiterContact.email == email,
            )
            .first()
        )
        if exists:
            skipped += 1
            continue
        row = RecruiterContact(
            recruiter_name=name,
            company=a.company,
            email=email,
            application_id=a.id,
            notes=f"Imported from application #{a.id} ({a.position}). Auto-email: OFF.",
            last_contact=a.date_applied,
            follow_up_date=a.follow_up_date,
        )
        db.add(row)
        created += 1
    db.commit()
    return {
        "created": created,
        "skipped": skipped,
        "auto_email": False,
        "fabricated": False,
    }


def followups_due(db: Session, on: date | None = None) -> list[dict[str, Any]]:
    on = on or date.today()
    rows = db.query(RecruiterContact).filter(RecruiterContact.follow_up_date != None).all()  # noqa: E711
    return [_out(r) for r in rows if r.follow_up_date and r.follow_up_date <= on]


def _parse_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    return date.fromisoformat(str(value)[:10])


def _out(row: RecruiterContact) -> dict[str, Any]:
    return {
        "id": row.id,
        "recruiter": row.recruiter_name,
        "recruiter_name": row.recruiter_name,
        "company": row.company,
        "email": row.email,
        "phone": row.phone,
        "linkedin": row.linkedin,
        "last_contact": row.last_contact.isoformat() if row.last_contact else None,
        "follow_up_schedule": row.follow_up_date.isoformat() if row.follow_up_date else None,
        "follow_up_date": row.follow_up_date.isoformat() if row.follow_up_date else None,
        "notes": row.notes,
        "referral_opportunities": row.referral_opportunities,
        "application_id": row.application_id,
        "auto_email": False,
        "approval_required_for_outreach": True,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }
