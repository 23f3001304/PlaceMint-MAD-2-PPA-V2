"""Application-level error type.

Raising `ApiError` anywhere in a request turns into a clean JSON response via
the handler registered in `app.api.errors`; callers never build error bodies
by hand.
"""


class ApiError(Exception):
    def __init__(self, message: str, status: int = 400, payload: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.payload = payload or {}


class NotFoundError(ApiError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, status=404)


class ForbiddenError(ApiError):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status=403)


class ConflictError(ApiError):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, status=409)
