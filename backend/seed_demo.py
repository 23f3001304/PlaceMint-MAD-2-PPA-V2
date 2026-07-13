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
        google.description = (
            "One of the largest technology companies in the world, known for Search, Android, Chrome, "
            "YouTube, Google Cloud and a fast-growing line of AI products. Campus engineers join small "
            "teams with genuine ownership from their first weeks, backed by strong mentorship and a "
            "rigorous code-review culture, and work on systems that run at enormous scale. Hiring spans "
            "product engineering, infrastructure, machine learning and site reliability, with structured "
            "onboarding and a clear path from intern to full-time."
        )

        msft = _company("careers@microsoft.demo", "Microsoft", "Software", "Hyderabad", ApprovalStatus.APPROVED)
        msft.website = "https://careers.microsoft.com"
        msft.links = [{"label": "Careers", "url": "https://careers.microsoft.com"}]
        msft.people = [{"name": "Satya Nadella", "role": "Chairman & CEO", "url": "https://linkedin.com/in/satyanadella"}]
        msft.description = (
            "A global software and cloud company behind Azure, Windows, Microsoft 365, GitHub, Xbox and a "
            "range of Copilot AI tools. Interns and new graduates ship real features alongside experienced "
            "engineers, in an environment that rewards curiosity, accessibility and long-term customer "
            "trust. Teams cover cloud infrastructure, developer tooling, security and applied AI, and new "
            "hires get a mentor, a learning budget and time to ramp up properly."
        )

        amazon = _company("careers@amazon.demo", "Amazon", "E-commerce", "Bengaluru", ApprovalStatus.APPROVED)
        amazon.website = "https://amazon.jobs"
        amazon.links = [{"label": "amazon.jobs", "url": "https://amazon.jobs"}]
        amazon.people = [{"name": "Andy Jassy", "role": "CEO", "url": ""}]
        amazon.description = (
            "A technology and commerce company whose engineering culture centres on the customer and on "
            "owning services end to end - designing, building, deploying and operating them. Work spans "
            "retail systems, AWS cloud, devices, logistics and advertising, frequently at a scale that is "
            "hard to find elsewhere. Expect high autonomy, a strong operational bar, real on-call "
            "ownership, and the growth that comes from seeing your work reach millions of people quickly."
        )

        meta = _company("careers@meta.demo", "Meta", "Software", "Gurugram", ApprovalStatus.PENDING)
        meta.website = "https://metacareers.com"
        meta.description = (
            "The company behind Facebook, Instagram, WhatsApp and Messenger, now investing heavily in AI "
            "and new computing platforms. Engineers work in a fast, bottom-up culture where individual "
            "impact is visible and shipping quickly is the norm, supported by some of the largest "
            "distributed systems in operation. Roles span product engineering, infrastructure, AI research "
            "and hardware, with strong mentorship for early-career engineers."
        )

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
        m_pe = _drive(meta, "PE Intern", "Production Engineer Intern", ["CSE"], 8.0, [2026, 2027], 26, ["Linux", "Python"], DriveStatus.PENDING, 25)

        g_swe.job_description = (
            "A 10 to 12 week summer internship embedded in a full-time engineering team. You will take a "
            "real project from design through to a shipped, code-reviewed change, with the internship "
            "structured as a path to a return offer. We care about solid fundamentals in data structures, "
            "algorithms and one core language far more than a long resume. Expect a dedicated host and "
            "mentor, weekly 1:1s, intern tech talks, and hands-on work with production systems.\n\n"
            "What you will do:\n"
            "- Own a scoped project end to end with support from your host\n"
            "- Write, test and review production code with the team\n"
            "- Present your work and results at the end of the internship"
        )
        g_l3.job_description = (
            "A full-time entry-level engineering role (L3) for 2026 graduates. You will join a team "
            "building and operating large-scale systems, own features end to end, and grow through code "
            "review, design discussions and mentorship. Strong problem-solving, comfort with C++, Java or "
            "Go, and an interest in distributed systems or ML infrastructure will serve you well. The role "
            "includes competitive compensation, relocation support and a clear early-career growth ladder."
        )
        m_sde.job_description = (
            "An internship on a product or platform team spanning Azure, Windows, Microsoft 365 or "
            "developer tools. You will scope and build a real feature with a mentor, take part in design "
            "and code reviews, and present your work at the end of the term, with strong intern-to-"
            "full-time conversion. We look for clear fundamentals, curiosity and collaboration over "
            "buzzwords. Includes mentorship, a learning budget and an inclusive, accessible team culture."
        )
        a_sde.job_description = (
            "A full-time software development role where you own services end to end - design, build, "
            "deploy and operate them in production. Expect high autonomy, a strong bar for operational "
            "excellence, and the chance to work across retail, AWS or devices at a scale that surfaces "
            "hard, interesting problems. We value strong coding fundamentals, systems thinking and a "
            "customer-first mindset. On-call and ownership are real, and so is the growth that comes with them."
        )
        m_pe.job_description = (
            "A hybrid software-and-systems internship: you will write code and also keep large services "
            "reliable, fast and efficient at scale. Projects range from automation and tooling to "
            "performance and reliability work, mentored by a production engineer and shipped to real "
            "infrastructure. Comfort with Linux, a scripting language, and curiosity about how systems "
            "behave under load is ideal. The team runs a fast, bottom-up culture with highly visible impact."
        )

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
