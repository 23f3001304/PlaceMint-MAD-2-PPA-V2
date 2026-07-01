"""Uniform JSON response envelope.

Success -> {"ok": true, "data": ...}; failure -> {"ok": false, "error": ...}.
Keeping one shape means the Vue API client only needs to unwrap `.data`.
"""
from flask import jsonify


def ok(data=None, status: int = 200, **extra):
    body = {"ok": True}
    if data is not None:
        body["data"] = data
    body.update(extra)
    return jsonify(body), status


def created(data=None, **extra):
    return ok(data, status=201, **extra)


def fail(message: str, status: int = 400, **extra):
    body = {"ok": False, "error": message}
    body.update(extra)
    return jsonify(body), status


def paginated(items, total: int, page: int, per_page: int):
    """Success envelope carrying pagination metadata alongside the rows."""
    pages = (total + per_page - 1) // per_page if per_page else 0
    return ok(items, total=total, page=page, per_page=per_page, pages=pages)
