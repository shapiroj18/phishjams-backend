import datetime
import os
from flask import render_template
from flask_mail import Message

from . import celery
from app import app, mail, db
from app.models import Subscribers, MJMAlerts
from ..api_tasks import phishnet_api, phishin_api

from twilio.rest import Client


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
        mail.send(msg)

    return "Mail sent"


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


@celery.task(name="mjm_notifications")
def mjm_notifications():

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    client = Client(account_sid, auth_token)

    # query all with mjm_alerts=True
    subs = MJMAlerts.query.filter_by(mjm_alerts=True)

    for subscriber in subs:
        if subscriber.mjm_alerts == True:
            message = client.messages.create(
                body=f"Mystery Jam Monday will be posted soon!\nphish.net",
                from_=os.environ["TWILIO_NUMBER"],
                to=subscriber.json_response["From"],
            )


@celery.task(name="support_notifications")
def support_notifications():

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    client = Client(account_sid, auth_token)

    # query all with subscribed=True
    subs = Subscribers.query.filter_by(subscribed=True)

    with app.app_context():
        for subscriber in subs:
            if subscriber.number_support_texts < 3:
                number_of_messages_left = 2 - subscriber.number_support_texts
                if number_of_messages_left >= 2:
                    lang_times = f"Don't worry, you'll only see this message {number_of_messages_left} more times"
                elif number_of_messages_left == 1:
                    lang_times = f"Don't worry, you'll only see this message {number_of_messages_left} more time"
                else:
                    lang_times = (
                        "Don't worry, this is the last time you'll see this message"
                    )
                message = client.messages.create(
                    body=f"If you want to support the development of this project, please consider contributing!\nhttps://ko-fi.com/shapiroj18\nhttps://www.patreon.com/shapiro18\n{lang_times}.",
                    from_=os.environ["TWILIO_NUMBER"],
                    to=subscriber.phone_number,
                )

                subscriber.number_support_texts += 1

        db.session.commit()
