"""Redis cache helpers: read-through caching with cache-key management.

Every read goes through `get_or_set` (value cached under a stable key with a
TTL); writes call the matching `invalidate_*`. If Redis is unreachable the
helpers compute directly and log at debug, so the app still serves (degraded)
rather than erroring on a cache outage.
"""
from flask import current_app

from app.extensions import cache

STATS_TTL = 60
LIST_TTL = 30


def _safe(action, *args, **kwargs):
    try:
        return action(*args, **kwargs), True
    except Exception as exc:  # Redis down / misconfigured: degrade, don't crash
        current_app.logger.debug("cache unavailable: %s", exc)
        return None, False


def get_or_set(key, ttl, producer):
    value, ok = _safe(cache.get, key)
    if ok and value is not None:
        return value
    value = producer()
    _safe(cache.set, key, value, timeout=ttl)
    return value


def _delete(key):
    _safe(cache.delete, key)


def admin_counts_key():
    return "stats:admin:counts"


def admin_charts_key():
    return "stats:admin:charts"


def company_stats_key(company_id):
    return f"stats:company:{company_id}"


def student_stats_key(student_id):
    return f"stats:student:{student_id}"


def organizations_key():
    return "list:organizations"


def invalidate_admin():
    _delete(admin_counts_key())
    _delete(admin_charts_key())
    _delete(organizations_key())


def invalidate_company(company_id):
    _delete(company_stats_key(company_id))
    invalidate_admin()


def invalidate_student(student_id):
    _delete(student_stats_key(student_id))
    invalidate_admin()
