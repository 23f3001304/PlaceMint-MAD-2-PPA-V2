"""Aggregate every model so `import app.models` registers all tables.

Import order matters only in that all classes must be imported before
`db.create_all()` runs; the app factory imports this package for that reason.
"""
from app.models.export_job import ExportJob
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.placement.placement import Placement
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.models.user import User

__all__ = [
    "User",
    "StudentProfile",
    "CompanyProfile",
    "PlacementDrive",
    "Application",
    "Placement",
    "ExportJob",
]
