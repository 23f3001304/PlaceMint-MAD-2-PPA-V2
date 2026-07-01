"""Placement: a finalized hire, created when a student is marked as placed.

Kept separate from Application so a student's confirmed placement history is a
first-class record (position, salary, joining date, offer letter) independent
of the application pipeline.
"""
from app.extensions import db
from app.models.base import TimestampMixin


class Placement(db.Model, TimestampMixin):
    __tablename__ = "placements"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id"), nullable=False, index=True
    )
    company_id = db.Column(
        db.Integer, db.ForeignKey("company_profiles.id"), nullable=False, index=True
    )
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"))
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), unique=True
    )

    position = db.Column(db.String(160), nullable=False)
    salary_lpa = db.Column(db.Float, default=0.0)
    joining_date = db.Column(db.Date)
    offer_letter_path = db.Column(db.String(255))

    student = db.relationship("StudentProfile", back_populates="placements")
    company = db.relationship("CompanyProfile", back_populates="placements")
    drive = db.relationship("PlacementDrive")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "student_id": self.student_id,
            "company_id": self.company_id,
            "drive_id": self.drive_id,
            "application_id": self.application_id,
            "position": self.position,
            "salary_lpa": self.salary_lpa,
            "joining_date": self.joining_date.isoformat() if self.joining_date else None,
            "company_name": self.company.company_name if self.company else None,
            "student_name": self.student.name if self.student else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
