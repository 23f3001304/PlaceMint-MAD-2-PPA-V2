"""Application: a student's record of applying to a drive.

The UNIQUE(student_id, drive_id) constraint enforces "apply once per drive"
at the database level, so duplicates are impossible even under a race.
"""
from app.extensions import db
from app.models.base import TimestampMixin, utcnow
from app.models.constants import ApplicationStatus


class Application(db.Model, TimestampMixin):
    __tablename__ = "applications"
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id"), nullable=False, index=True
    )
    drive_id = db.Column(
        db.Integer, db.ForeignKey("placement_drives.id"), nullable=False, index=True
    )

    applied_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    status = db.Column(
        db.String(20), default=ApplicationStatus.APPLIED, nullable=False, index=True
    )
    interview_at = db.Column(db.DateTime)
    interview_mode = db.Column(db.String(40))  # e.g. "In-person", "Online"
    remarks = db.Column(db.String(255))

    student = db.relationship("StudentProfile", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")

    def to_dict(self, include_drive: bool = True, include_student: bool = False) -> dict:
        data = {
            "id": self.id,
            "student_id": self.student_id,
            "drive_id": self.drive_id,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "interview_at": self.interview_at.isoformat() if self.interview_at else None,
            "interview_mode": self.interview_mode,
            "remarks": self.remarks,
        }
        if include_drive and self.drive:
            data["drive"] = self.drive.to_dict(include_company=True)
        if include_student and self.student:
            data["student"] = self.student.to_dict()
        return data
