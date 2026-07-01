"""Domain enumerations as named constants.

Storing these as validated strings keeps the SQLite schema simple while
avoiding the "stringly-typed" anti-pattern: call sites use the constant,
never a bare literal.
"""


class Role:
    ADMIN = "admin"
    COMPANY = "company"
    STUDENT = "student"
    ALL = frozenset({ADMIN, COMPANY, STUDENT})
    REGISTERABLE = frozenset({COMPANY, STUDENT})  # admin is seeded, never registered


class ApprovalStatus:
    """Lifecycle of a company's registration."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ALL = frozenset({PENDING, APPROVED, REJECTED})


class DriveStatus:
    """Lifecycle of a placement drive / job posting.

    `pending`  awaiting admin approval
    `approved` live and visible to eligible students (i.e. "Active")
    `rejected` refused by admin
    `closed`   company stopped accepting applications
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"
    ALL = frozenset({PENDING, APPROVED, REJECTED, CLOSED})
    # Statuses the owning company may toggle once admin has approved.
    COMPANY_SETTABLE = frozenset({APPROVED, CLOSED})


class ApplicationStatus:
    """Lifecycle of a student's application to a drive.

    Pipeline: applied -> shortlisted -> interview -> offer -> placed,
    with `rejected` reachable from any stage.
    """

    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    PLACED = "placed"
    ALL = frozenset({APPLIED, SHORTLISTED, INTERVIEW, OFFER, REJECTED, PLACED})
    # Statuses a company may assign when moving an application forward.
    COMPANY_SETTABLE = frozenset({SHORTLISTED, INTERVIEW, OFFER, REJECTED, PLACED})
    # Ordered stages for the application-funnel analytics chart.
    PIPELINE = (APPLIED, SHORTLISTED, INTERVIEW, OFFER, PLACED)
