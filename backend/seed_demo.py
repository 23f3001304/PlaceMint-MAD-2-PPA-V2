"""Populate the database with demo data for local testing and demos.

Idempotent: does nothing if the demo companies already exist. Run with the
venv active:  python seed_demo.py   (all demo logins use password "password123")
"""
from datetime import date, timedelta

from app import create_app
from app.auth.passwords import hash_password
from app.extensions import db
from app.models.constants import ApplicationStatus, ApprovalStatus, DriveStatus, Role
from app.models.placement.application import Application
from app.models.placement.drive import PlacementDrive
from app.models.placement.placement import Placement
from app.models.profiles.company import CompanyProfile
from app.models.profiles.student import StudentProfile
from app.models.user import User

PW = hash_password("password123")


def _company(email, name, industry, location, status):
    user = User(email=email, password_hash=PW, role=Role.COMPANY)
    user.company_profile = CompanyProfile(
        company_name=name, industry=industry, location=location,
        approval_status=status, hr_contact=f"hr@{email.split('@')[1]}",
        description=f"{name} hires from campus every year.",
    )
    db.session.add(user)
    return user.company_profile


def _student(email, name, roll, branch, cgpa, year, skills):
    user = User(email=email, password_hash=PW, role=Role.STUDENT)
    user.student_profile = StudentProfile(
        name=name, roll_no=roll, branch=branch, cgpa=cgpa, grad_year=year,
        degree="B.Tech", skills=skills, onboarded=True,
    )
    db.session.add(user)
    return user.student_profile


def _drive(company, drive_name, title, branches, cgpa, years, pkg, skills, status, days):
    drive = PlacementDrive(
        company=company, drive_name=drive_name, job_title=title,
        job_description=f"{title} role at {company.company_name}. Great team, real impact.",
        eligible_branches=branches, min_cgpa=cgpa, eligible_years=years,
        package_lpa=pkg, skills_required=skills, min_experience=0,
        location=company.location, status=status,
        deadline=date.today() + timedelta(days=days),
    )
    db.session.add(drive)
    return drive


def seed():
    with create_app().app_context():
        if CompanyProfile.query.filter_by(company_name="TechNova").first():
            print("Demo data already present.")
            return

        tech = _company("tech@demo.com", "TechNova", "Software", "Bengaluru", ApprovalStatus.APPROVED)
        data = _company("data@demo.com", "DataForge", "Analytics", "Hyderabad", ApprovalStatus.APPROVED)
        _company("build@demo.com", "BuildRight", "Core Engineering", "Pune", ApprovalStatus.PENDING)

        tech.website = "https://technova.example"
        tech.links = [
            {"label": "LinkedIn", "url": "https://linkedin.com/company/technova"},
            {"label": "Careers", "url": "https://technova.example/careers"},
        ]
        tech.people = [
            {"name": "Riya Kapoor", "role": "CEO", "url": "https://linkedin.com/in/riyakapoor"},
            {"name": "Sequoia India", "role": "Lead investor", "url": "https://www.sequoiacap.com"},
        ]
        data.website = "https://dataforge.example"
        data.people = [{"name": "Arvind Rao", "role": "Founder & CEO", "url": ""}]

        s = [
            _student("ada@demo.com", "Ada Iyer", "CS23B001", "CSE", 8.9, 2026, ["Python", "React", "SQL"]),
            _student("rahul@demo.com", "Rahul Nair", "CS23B002", "CSE", 7.2, 2026, ["Java", "SQL"]),
            _student("sara@demo.com", "Sara Khan", "EC23B003", "ECE", 8.1, 2026, ["C++", "MATLAB"]),
            _student("meera@demo.com", "Meera Das", "DS23B004", "Data Science", 9.1, 2026, ["Python", "SQL", "ML"]),
            _student("arjun@demo.com", "Arjun Menon", "AI23B005", "AI & ML", 7.8, 2027, ["Python", "PyTorch"]),
        ]
        s[0].links = [
            {"label": "LinkedIn", "url": "https://linkedin.com/in/adaiyer"},
            {"label": "GitHub", "url": "https://github.com/adaiyer"},
        ]

        d_sde = _drive(tech, "Summer SDE 2026", "SDE Intern", ["CSE", "AI & ML"], 7.0, [2026, 2027], 12, ["Python", "React"], DriveStatus.APPROVED, 20)
        d_be = _drive(tech, "Backend Hire", "Backend Engineer", ["CSE"], 7.5, [2026], 18, ["Python", "SQL"], DriveStatus.APPROVED, 12)
        d_da = _drive(data, "Analytics Drive", "Data Analyst", ["Data Science", "CSE", "AI & ML"], 7.5, [2026], 14, ["SQL", "Python"], DriveStatus.APPROVED, 8)
        _drive(data, "ML Intern Hunt", "ML Intern", ["AI & ML", "Data Science"], 8.0, [2026, 2027], 10, ["Python"], DriveStatus.PENDING, 25)

        db.session.flush()
        db.session.add_all([
            Application(student=s[0], drive=d_sde, status=ApplicationStatus.SHORTLISTED),
            Application(student=s[0], drive=d_be, status=ApplicationStatus.APPLIED),
            Application(student=s[1], drive=d_sde, status=ApplicationStatus.APPLIED),
            Application(student=s[3], drive=d_da, status=ApplicationStatus.PLACED),
            Application(student=s[4], drive=d_sde, status=ApplicationStatus.APPLIED),
            Application(student=s[4], drive=d_da, status=ApplicationStatus.SHORTLISTED),
        ])
        db.session.add(Placement(
            student=s[3], company=data, drive=d_da, position="Data Analyst",
            salary_lpa=14, joining_date=date.today() + timedelta(days=120),
        ))
        db.session.commit()
        print("Seeded demo data: 3 companies, 5 students, 4 drives, 6 applications, 1 placement.")


if __name__ == "__main__":
    seed()
