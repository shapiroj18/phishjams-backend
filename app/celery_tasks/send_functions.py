import datetime
from flask import render_template
from flask_mail import Message

from . import celery
from app import app, mail, db
from app.models import Subscribers
from ..api_tasks import phishnet_api, phishin_api


phishnet_api = phishnet_api.PhishNetAPI()
phishin_api = phishin_api.PhishINAPI()


@celery.task(name="email_send")
def email_send():
    song, date = phishnet_api.get_random_jamchart()
    jam_url = phishin_api.get_song_url(song=song, date=date)
    relisten_formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
        "%Y/%m/%d"
    )
    phishnet_url = phishnet_api.get_show_url(date)

    with app.app_context():
        msg = Message(
            subject="Daily Phish Jam",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=["shapiroj18@gmail.com"],
        )
        msg.html = render_template(
            "random_jam_email.html",
            song=song,
            date=date,
            jam_url=jam_url,
            relisten_formatted_date=relisten_formatted_date,
            phishnet_url=phishnet_url,
        )
        return mail.send(msg)


@celery.task(name="daily_email_send")
def daily_email_sends():

    # query all with subscribed=True
    subs = Subscribers.query.filter_by(subscribed=True)

    song, date = phishnet_api.get_random_jamchart()
    jam_url = phishin_api.get_song_url(song=song, date=date)
    relisten_formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
        "%Y/%m/%d"
    )
    phishnet_url = phishnet_api.get_show_url(date)

    with app.app_context():
        with mail.connect() as conn:
            for subscriber in subs:
                msg = Message(
                    subject="Daily Phish Jam",
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=[subscriber.email],
                )
                msg.html = render_template(
                    "random_jam_email.html",
                    song=song,
                    date=date,
                    jam_url=jam_url,
                    relisten_formatted_date=relisten_formatted_date,
                    phishnet_url=phishnet_url,
                )
                conn.send(msg)

    return "Mail sent"
