"""Student-specific profile, one row per student user."""
from app.extensions import db
from app.models.base import TimestampMixin


class StudentProfile(db.Model, TimestampMixin):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    name = db.Column(db.String(120), nullable=False)
    roll_no = db.Column(db.String(40), unique=True, nullable=False, index=True)
    branch = db.Column(db.String(60), nullable=False, index=True)
    degree = db.Column(db.String(80))  # e.g. "B.Tech", "M.Sc"
    cgpa = db.Column(db.Float, default=0.0, nullable=False)
    grad_year = db.Column(db.Integer, nullable=False, index=True)
    phone = db.Column(db.String(20))
    skills = db.Column(db.JSON, default=list)  # e.g. ["Python", "SQL"]
    experience = db.Column(db.Text)  # legacy free text / resume-parsed notes
    experiences = db.Column(db.JSON, default=list)  # [{title, org, period, description}]
    projects = db.Column(db.JSON, default=list)  # up to 3 {title, link, period, description}
    links = db.Column(db.JSON, default=list)  # up to 3 {label, url} social links
    resume_path = db.Column(db.String(255))
    onboarded = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship(
        "Application", back_populates="student", cascade="all, delete-orphan"
    )
    placements = db.relationship(
        "Placement", back_populates="student", cascade="all, delete-orphan"
    )

    @property
    def is_complete(self) -> bool:
        """Enough profile to be evaluated for eligibility (CGPA is the key field)."""
        return bool(self.cgpa and self.cgpa > 0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.user.email if self.user else None,
            "name": self.name,
            "roll_no": self.roll_no,
            "branch": self.branch,
            "degree": self.degree,
            "cgpa": self.cgpa,
            "grad_year": self.grad_year,
            "phone": self.phone,
            "skills": self.skills or [],
            "experience": self.experience,
            "experiences": self.experiences or [],
            "projects": self.projects or [],
            "links": self.links or [],
            "has_resume": bool(self.resume_path),
            "onboarded": self.onboarded,
            "profile_complete": self.is_complete,
            "is_active": self.user.is_active if self.user else True,
            "is_blacklisted": self.user.is_blacklisted if self.user else False,
        }
