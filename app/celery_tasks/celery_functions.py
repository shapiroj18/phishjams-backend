import datetime
import os
from flask import render_template
from flask_mail import Message
from dotenv import load_dotenv


from . import celery
from app import app, mail, db
from app.models import Subscribers, MJMAlerts, PhishJamsQueue
from ..api_tasks import phishnet_api, phishin_api

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
phishnet_api = phishnet_api.PhishNetAPI()
phishin_api = phishin_api.PhishINAPI()


@celery.task(name="email_send_test")
def email_send_test():
    song, date = phishnet_api.get_random_jamchart()
    jam_url = phishin_api.get_song_url(song=song, date=date)
    relisten_formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
        "%Y/%m/%d"
    )
    phishnet_url = phishnet_api.get_show_url(date)

    with app.app_context():
        msg = Message(
            subject="Daily Phish Jam",
            sender=os.getenv("SENDGRID_MAIL_SENDER"),
            recipients=["shapiroj18@gmail.com"],
        )
        msg.html = render_template(
            "random_jam_email.html",
            song=song,
            date=date,
            jam_url=jam_url,
            relisten_formatted_date=relisten_formatted_date,
            phishnet_url=phishnet_url,
            web_url=os.getenv("WEB_URL"),
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
                    sender=os.getenv("SENDGRID_MAIL_SENDER"),
                    recipients=[subscriber.email],
                )
                msg.html = render_template(
                    "random_jam_email.html",
                    song=song,
                    date=date,
                    jam_url=jam_url,
                    relisten_formatted_date=relisten_formatted_date,
                    phishnet_url=phishnet_url,
                    web_url=os.getenv("WEB_URL"),
                )
                conn.send(msg)

    return "Mail sent"


@celery.task(name="mjm_notifications")
def mjm_notifications():

    bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))

    # query all with mjm_alerts
    subs = MJMAlerts.query.filter_by(mjm_alerts=True)

    for subscriber in subs:
        if subscriber.mjm_alerts:

            keyboard = [
                [
                    InlineKeyboardButton("Phish.Net", url="https://phish.net/"),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            bot.send_message(
                chat_id=subscriber.telegram_chat_id,
                text=f"Get ready, Mystery Jam Monday is about to be posted!",
                reply_markup=reply_markup,
            )


@celery.task(name="support_notifications")
def support_notifications():

    bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))

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

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Ko-Fi", url="https://ko-fi.com/shapiroj18"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "GitHub", url="https://github.com/sponsors/shapiroj18"
                        ),
                    ],
                ]

                reply_markup = InlineKeyboardMarkup(keyboard)

                bot.send_message(
                    chat_id=subscriber.telegram_chat_id,
                    text=f"This bot is not cheap to build! If you want to support the development of this project, please consider contributing. {lang_times}.",
                    reply_markup=reply_markup,
                )

                subscriber.number_support_texts += 1

        db.session.commit()


@celery.task(name="delete_queue_records")
def delete_queue_records():
    """
    Deletes all records of the queue table
    """
    db.session.query(PhishJamsQueue).delete()
    db.session.commit()

    return "Records deleted"


# @celery.task(name="print_date")
# def print_date():
#     print(datetime.datetime.now())
