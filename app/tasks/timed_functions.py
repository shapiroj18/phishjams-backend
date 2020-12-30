from . import celery


@celery.task(name="celery_example.reverse")
def reverse(string):
    return string[::-1]
