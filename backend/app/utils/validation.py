"""Small boundary validators.

Every API handler runs untrusted input through these before it reaches a
service, so services can trust the shapes they receive (dev-principles: validate
at the edge, trust internally).
"""
import re

from app.utils.errors import ApiError

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require(data: dict, *fields: str) -> None:
    missing = [f for f in fields if data.get(f) in (None, "", [])]
    if missing:
        raise ApiError("Missing required fields: " + ", ".join(missing))


def valid_email(email: str) -> None:
    if not EMAIL_RE.match((email or "").strip()):
        raise ApiError("Invalid email address")


def as_float(value, field: str, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ApiError(f"{field} must be a number")


def as_int(value, field: str, default=None) -> int:
    if value in (None, "") and default is not None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ApiError(f"{field} must be an integer")


def as_list(value) -> list:
    """Accept a JSON array or a comma-separated string; return a clean list."""
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [part.strip() for part in str(value).split(",") if part.strip()]


def clean_links(value, cap: int) -> list:
    """Normalize a list of {label, url} links: force a scheme, derive a missing
    label from the host, and cap the count (student profiles 3, company 4)."""
    out = []
    for item in value or []:
        if not isinstance(item, dict):
            continue
        url = (item.get("url") or "").strip()
        if not url:
            continue
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        label = (item.get("label") or "").strip() or url.split("//", 1)[-1].split("/", 1)[0]
        out.append({"label": label[:40], "url": url[:200]})
        if len(out) >= cap:
            break
    return out


def clean_phone(value):
    """Sanitize and validate an Indian mobile number: strip non-digits, drop a
    +91/0 prefix, and require 10 digits starting 6-9. Empty is allowed (None)."""
    raw = (value or "").strip()
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    if not re.fullmatch(r"[6-9]\d{9}", digits):
        raise ApiError("Enter a valid Indian mobile number (10 digits starting 6-9)")
    return digits


def clean_experiences(value, cap: int = 8) -> list:
    """Normalize experience entries {title, org, period, description}; a title is
    required, the rest is trimmed and length-capped, and the list count is capped."""
    out = []
    for item in value or []:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or "").strip()
        if not title:
            continue
        out.append({
            "title": title[:120],
            "org": (item.get("org") or "").strip()[:120],
            "period": (item.get("period") or "").strip()[:60],
            "description": (item.get("description") or "").strip()[:1000],
        })
        if len(out) >= cap:
            break
    return out


def clean_projects(value, cap: int = 3) -> list:
    """Normalize project entries {title, link, period, description}; a title is
    required, any link gets a scheme, and the list count is capped (students: 3)."""
    out = []
    for item in value or []:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or "").strip()
        if not title:
            continue
        link = (item.get("link") or "").strip()
        if link and not link.startswith(("http://", "https://")):
            link = "https://" + link
        out.append({
            "title": title[:120],
            "link": link[:200],
            "period": (item.get("period") or "").strip()[:60],
            "description": (item.get("description") or "").strip()[:1000],
        })
        if len(out) >= cap:
            break
    return out


def clean_people(value, cap: int) -> list:
    """Normalize key-people entries {name, role, url} (a company's CEO, investor,
    etc.); require a name, force a scheme on any link, and cap the count."""
    out = []
    for item in value or []:
        if not isinstance(item, dict):
            continue
        name = (item.get("name") or "").strip()
        if not name:
            continue
        url = (item.get("url") or "").strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        out.append({"name": name[:80], "role": (item.get("role") or "").strip()[:60], "url": url[:200]})
        if len(out) >= cap:
            break
    return out
