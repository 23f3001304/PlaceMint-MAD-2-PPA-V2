"""Placement drive: a job posting a company runs after admin approval."""
from app.extensions import db
from app.models.base import TimestampMixin
from app.models.constants import DriveStatus


class PlacementDrive(db.Model, TimestampMixin):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer, db.ForeignKey("company_profiles.id"), nullable=False, index=True
    )

    job_title = db.Column(db.String(160), nullable=False, index=True)
    job_description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(120))
    package_lpa = db.Column(db.Float, default=0.0)  # salary in LPA
    benefits = db.Column(db.Text)

    # Eligibility / requirements. Lists are stored as JSON (TEXT) in SQLite.
    skills_required = db.Column(db.JSON, default=list)  # e.g. ["Python", "React"]
    min_experience = db.Column(db.Float, default=0.0)  # years
    eligible_branches = db.Column(db.JSON, default=list)  # e.g. ["CSE", "ECE"]
    min_cgpa = db.Column(db.Float, default=0.0)
    eligible_years = db.Column(db.JSON, default=list)  # e.g. [2025, 2026]

    deadline = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(
        db.String(20), default=DriveStatus.PENDING, nullable=False, index=True
    )

    company = db.relationship("CompanyProfile", back_populates="drives")
    applications = db.relationship(
        "Application", back_populates="drive", cascade="all, delete-orphan"
    )

    def to_dict(self, include_company: bool = True) -> dict:
        data = {
            "id": self.id,
            "company_id": self.company_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "location": self.location,
            "package_lpa": self.package_lpa,
            "benefits": self.benefits,
            "skills_required": self.skills_required or [],
            "min_experience": self.min_experience,
            "eligible_branches": self.eligible_branches or [],
            "min_cgpa": self.min_cgpa,
            "eligible_years": self.eligible_years or [],
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
            "applicant_count": len(self.applications),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_company and self.company:
            data["company_name"] = self.company.company_name
            data["industry"] = self.company.industry
        return data
