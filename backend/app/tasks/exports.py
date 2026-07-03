"""User-triggered CSV export task (thin wrapper over the export service)."""
from celery import shared_task

from app.services.exports.csv_export import build_export


@shared_task(name="app.tasks.exports.run_export")
def run_export(export_job_id: int) -> dict:
    return build_export(export_job_id)
