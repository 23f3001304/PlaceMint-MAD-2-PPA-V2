"""JWT wiring: string identities and JSON responses for auth failures.

The role travels as an additional claim set at token-creation time (see the
auth service), so authorization checks never need a database round-trip.
"""
from flask import jsonify


def register_jwt_handlers(jwt) -> None:
    @jwt.user_identity_loader
    def _identity(user_id):
        # The JWT "sub" claim must be a string.
        return str(user_id)

    @jwt.unauthorized_loader
    def _missing(_reason):
        return jsonify({"ok": False, "error": "Authentication required"}), 401

    @jwt.invalid_token_loader
    def _invalid(_reason):
        return jsonify({"ok": False, "error": "Invalid token"}), 401

    @jwt.expired_token_loader
    def _expired(_header, _payload):
        return jsonify({"ok": False, "error": "Session expired, please log in"}), 401
