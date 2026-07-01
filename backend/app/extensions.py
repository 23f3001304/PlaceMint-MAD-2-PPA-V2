"""Flask extension singletons.

Kept in their own module so both the app factory and the models can import
them without creating circular imports.
"""
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()
