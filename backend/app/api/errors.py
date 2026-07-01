"""Translate exceptions into JSON so the SPA always receives a parseable body."""
from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.utils.errors import ApiError


def register_error_handlers(app):
    @app.errorhandler(ApiError)
    def _handle_api_error(err: ApiError):
        return jsonify({"ok": False, "error": err.message, **err.payload}), err.status

    @app.errorhandler(HTTPException)
    def _handle_http_error(err: HTTPException):
        return jsonify({"ok": False, "error": err.description}), err.code

    # In production, swallow unexpected errors behind a generic 500 (no stack
    # leak). In debug we let them propagate to Flask's interactive debugger.
    if not app.debug:
        @app.errorhandler(Exception)
        def _handle_unexpected(err: Exception):
            app.logger.exception("Unhandled exception")
            return jsonify({"ok": False, "error": "Internal server error"}), 500
