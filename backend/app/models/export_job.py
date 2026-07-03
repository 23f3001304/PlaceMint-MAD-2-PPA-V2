"""Tracks an async CSV export so its status survives across processes.

The web request creates the row (pending) and enqueues the task; the Celery
worker updates it to running/done. The SPA polls its status by id.
"""
from app.extensions import db
from app.models.base import TimestampMixin


class ExportJob(db.Model, TimestampMixin):
    __tablename__ = "export_jobs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)  # pending|running|done|failed
    filename = db.Column(db.String(255))
    row_count = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role": self.role,
            "status": self.status,
            "ready": self.status == "done",
            "filename": self.filename,
            "row_count": self.row_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
