"""Celery entry point.

Run the worker and beat together (Windows-friendly):
    celery -A celery_worker.celery worker --pool=solo -B --loglevel=info
"""
from app import create_app

flask_app = create_app()
celery = flask_app.extensions["celery"]
