"""Password hashing helpers.

Thin wrappers over Werkzeug (ships with Flask) so the rest of the codebase
never touches the raw hashing API and no other library is required.
"""
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(plaintext: str) -> str:
    return generate_password_hash(plaintext)


def verify_password(password_hash: str, plaintext: str) -> bool:
    return check_password_hash(password_hash, plaintext)
