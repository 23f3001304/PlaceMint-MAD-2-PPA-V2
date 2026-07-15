"""Celery integration with the Flask app factory.

`make_celery(app)` builds a Celery bound to the app (tasks run inside an app
context) and wires the beat schedule. In testing, tasks run eagerly so the
export flow can be exercised without a broker.
"""
from celery import Celery, Task
from celery.schedules import crontab


def make_celery(flask_app) -> Celery:
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery("ppa", task_cls=ContextTask)
    celery.conf.update(
        broker_url=flask_app.config["REDIS_URL"],
        result_backend=flask_app.config["REDIS_URL"],
        broker_connection_retry_on_startup=True,
        task_always_eager=flask_app.config.get("CELERY_TASK_ALWAYS_EAGER", False),
        task_eager_propagates=True,
        timezone="UTC",
        beat_schedule={
            "daily-reminders": {
                "task": "app.tasks.reminders.send_daily_reminders",
                "schedule": crontab(hour=8, minute=0),
            },
            "monthly-reports": {
                "task": "app.tasks.reports.send_monthly_reports",
                "schedule": crontab(day_of_month=1, hour=6, minute=0),
            },
        },
    )
    celery.set_default()
    flask_app.extensions["celery"] = celery

    from app.tasks import exports, reminders, reports, mail  # noqa: F401  (register tasks)

    return celery
