"""Shared model building blocks."""
from datetime import datetime, timezone

from app.extensions import db


def utcnow() -> datetime:
    """Timezone-aware current UTC time (avoids the naive-datetime pitfalls)."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Adds created/updated audit columns to a model."""

    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow, nullable=False)
