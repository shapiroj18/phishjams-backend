web: gunicorn phish_bot:app
worker: celery worker -A app.celery_tasks.celery --beat --loglevel=info