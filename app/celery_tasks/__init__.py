import os
from celery import Celery
from celery.schedules import crontab
from app import app


def make_celery(app):

    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app=app)

# Add periodic tasks
celery_beat_schedule = {
    "daily_email_send": {
        "task": "daily_email_send",
        "schedule": crontab(minute=59, hour=12),
    }
}

celery.conf.update(
    timezone="America/New_York",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    beat_schedule=celery_beat_schedule,
)


@celery.task
def test(arg):
    print(arg)
    return arg
