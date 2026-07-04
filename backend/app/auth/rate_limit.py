"""Fixed-window rate limiting.

Uses Redis when reachable (correct across multiple workers); otherwise falls
back to an in-process counter so a single dev server is still protected. The
control fails open (logs and allows) if both are unavailable, to favour
availability of auth over a hard lockout.
"""
import time
from functools import wraps

from flask import current_app, request
from redis import Redis

from app.utils.errors import ApiError

_redis = None
_local: dict[str, list] = {}


def _redis_client():
    global _redis
    if _redis is None:
        _redis = Redis.from_url(current_app.config["REDIS_URL"], socket_timeout=0.2)
    return _redis


def _hit_local(key: str, window: int) -> int:
    now = time.time()
    entry = _local.get(key)
    if entry is None or entry[1] < now:
        _local[key] = [1, now + window]
        return 1
    entry[0] += 1
    return entry[0]


def _count(key: str, window: int) -> int:
    try:
        client = _redis_client()
        count = client.incr(key)
        if count == 1:
            client.expire(key, window)
        return count
    except Exception:
        current_app.logger.debug("rate limiter: redis unavailable, using in-process store")
        return _hit_local(key, window)


def rate_limit(max_requests: int, window_seconds: int):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_app.config.get("RATELIMIT_ENABLED", True):
                return fn(*args, **kwargs)
            key = f"rl:{fn.__qualname__}:{request.remote_addr}"
            if _count(key, window_seconds) > max_requests:
                raise ApiError("Too many requests, please slow down and retry shortly", status=429)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
