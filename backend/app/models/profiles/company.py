"""Company-specific profile, one row per company user."""
from app.extensions import db
from app.models.base import TimestampMixin
from app.models.constants import ApprovalStatus


class CompanyProfile(db.Model, TimestampMixin):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    company_name = db.Column(db.String(160), nullable=False, index=True)
    industry = db.Column(db.String(80), index=True)
    location = db.Column(db.String(120))
    hr_contact = db.Column(db.String(120))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    approval_status = db.Column(
        db.String(20), default=ApprovalStatus.PENDING, nullable=False, index=True
    )

    user = db.relationship("User", back_populates="company_profile")
    drives = db.relationship(
        "PlacementDrive", back_populates="company", cascade="all, delete-orphan"
    )
    placements = db.relationship(
        "Placement", back_populates="company", cascade="all, delete-orphan"
    )

    @property
    def is_approved(self) -> bool:
        return self.approval_status == ApprovalStatus.APPROVED

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.user.email if self.user else None,
            "company_name": self.company_name,
            "industry": self.industry,
            "location": self.location,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "description": self.description,
            "approval_status": self.approval_status,
            "drive_count": len(self.drives),
            "is_active": self.user.is_active if self.user else True,
            "is_blacklisted": self.user.is_blacklisted if self.user else False,
        }
