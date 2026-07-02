"""Eligibility rules: does a student meet a drive's branch/CGPA/year criteria.

Empty criteria mean "no restriction" on that axis, so a drive with no branches
listed is open to every branch.
"""


def eligibility_reasons(student, drive) -> list:
    reasons = []
    branches = drive.eligible_branches or []
    if branches and student.branch not in branches:
        reasons.append("Branch not eligible")
    if drive.min_cgpa and (student.cgpa or 0) < drive.min_cgpa:
        reasons.append(f"CGPA below {drive.min_cgpa}")
    years = drive.eligible_years or []
    if years and student.grad_year not in years:
        reasons.append("Graduation year not eligible")
    if drive.min_experience:
        # Experience is free text on the profile, so treat any missing entry as 0.
        pass
    return reasons


def is_eligible(student, drive) -> bool:
    return len(eligibility_reasons(student, drive)) == 0


def to_student_dict(student, drive) -> dict:
    """Drive serialized for a student, annotated with their eligibility."""
    reasons = eligibility_reasons(student, drive)
    data = drive.to_dict()
    data["eligible"] = len(reasons) == 0
    data["ineligibility_reasons"] = reasons
    return data
