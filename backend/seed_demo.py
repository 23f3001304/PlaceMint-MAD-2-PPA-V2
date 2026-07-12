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
        approval_status=status, hr_contact=f"careers@{name.lower()}.demo",
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
        job_description=f"{title} at {company.company_name}. Real ownership, strong mentorship and impact from day one.",
        eligible_branches=branches, min_cgpa=cgpa, eligible_years=years,
        package_lpa=pkg, skills_required=skills, min_experience=0,
        location=company.location, status=status,
        deadline=date.today() + timedelta(days=days),
    )
    db.session.add(drive)
    return drive


def seed():
    with create_app().app_context():
        if CompanyProfile.query.filter_by(company_name="Google").first():
            print("Demo data already present.")
            return

        google = _company("careers@google.demo", "Google", "Software", "Bengaluru", ApprovalStatus.APPROVED)
        google.website = "https://careers.google.com"
        google.links = [
            {"label": "Careers", "url": "https://careers.google.com"},
            {"label": "LinkedIn", "url": "https://linkedin.com/company/google"},
        ]
        google.people = [
            {"name": "Sundar Pichai", "role": "CEO", "url": "https://linkedin.com/in/sundarpichai"},
            {"name": "Ruth Porat", "role": "President & CIO", "url": ""},
        ]
        google.description = "Google builds products that help billions of people. Campus hires ship on Search, Cloud, Android and AI."

        msft = _company("careers@microsoft.demo", "Microsoft", "Software", "Hyderabad", ApprovalStatus.APPROVED)
        msft.website = "https://careers.microsoft.com"
        msft.links = [{"label": "Careers", "url": "https://careers.microsoft.com"}]
        msft.people = [{"name": "Satya Nadella", "role": "Chairman & CEO", "url": "https://linkedin.com/in/satyanadella"}]
        msft.description = "Microsoft empowers every person and organization to achieve more, across Azure, Windows and Microsoft 365."

        amazon = _company("careers@amazon.demo", "Amazon", "E-commerce", "Bengaluru", ApprovalStatus.APPROVED)
        amazon.website = "https://amazon.jobs"
        amazon.links = [{"label": "amazon.jobs", "url": "https://amazon.jobs"}]
        amazon.people = [{"name": "Andy Jassy", "role": "CEO", "url": ""}]
        amazon.description = "Amazon is guided by customer obsession. Engineers own systems that serve millions at scale."

        meta = _company("careers@meta.demo", "Meta", "Software", "Gurugram", ApprovalStatus.PENDING)
        meta.website = "https://metacareers.com"
        meta.description = "Meta is building the future of connection, from apps used by billions to AI and the metaverse."

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
        s[0].experiences = [
            {"title": "Software Engineering Intern", "org": "Zomato", "period": "May-Jul 2024",
             "description": "Built internal React dashboards and shipped an API that cut report time by 40%."},
            {"title": "Open Source Contributor", "org": "CNCF", "period": "2023",
             "description": "Bug fixes and docs for a Kubernetes tooling project."},
        ]

        g_swe = _drive(google, "SWE Intern 2026", "Software Engineer Intern", ["CSE", "AI & ML", "Data Science"], 7.5, [2026, 2027], 24, ["Python", "Data Structures"], DriveStatus.APPROVED, 20)
        g_l3 = _drive(google, "Software Engineer L3", "Software Engineer", ["CSE"], 8.0, [2026], 32, ["C++", "System Design"], DriveStatus.APPROVED, 14)
        m_sde = _drive(msft, "SDE Intern", "SDE Intern", ["CSE", "ECE"], 7.0, [2026, 2027], 20, ["C#", "Algorithms"], DriveStatus.APPROVED, 10)
        a_sde = _drive(amazon, "SDE-1 Hire", "SDE-1", ["CSE", "Data Science", "AI & ML"], 7.5, [2026], 28, ["Java", "AWS"], DriveStatus.APPROVED, 8)
        _drive(meta, "PE Intern", "Production Engineer Intern", ["CSE"], 8.0, [2026, 2027], 26, ["Linux", "Python"], DriveStatus.PENDING, 25)

        db.session.flush()
        db.session.add_all([
            Application(student=s[0], drive=g_swe, status=ApplicationStatus.SHORTLISTED),
            Application(student=s[0], drive=g_l3, status=ApplicationStatus.APPLIED),
            Application(student=s[1], drive=g_swe, status=ApplicationStatus.APPLIED),
            Application(student=s[3], drive=a_sde, status=ApplicationStatus.PLACED),
            Application(student=s[4], drive=g_swe, status=ApplicationStatus.APPLIED),
            Application(student=s[4], drive=m_sde, status=ApplicationStatus.SHORTLISTED),
        ])
        db.session.add(Placement(
            student=s[3], company=amazon, drive=a_sde, position="SDE-1",
            salary_lpa=28, joining_date=date.today() + timedelta(days=120),
        ))
        db.session.commit()
        print("Seeded demo data: 4 companies, 5 students, 5 drives, 6 applications, 1 placement.")


if __name__ == "__main__":
    seed()
