import re
import os

from flask import request, jsonify
from app import app, mail, db
from app.models import Subscribers, MJMAlerts
from app.celery_tasks import send_functions
from flask import render_template
from flask_mail import Message

from app.api_tasks import phishnet_api, phishin_api
from twilio.twiml.messaging_response import MessagingResponse

phishnet_api = phishnet_api.PhishNetAPI()
phishin_api = phishin_api.PhishINAPI()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/radio")
def radio():
    return render_template("radio.html")

@app.route("/email")
def email():
    return send_functions.email_send()


@app.route("/subscribedailyjams", methods=["POST"])
def subscribedailyjams():
    try:
        email = request.values.get("email").lower()
        platform = request.values.get("platform").lower()
        chat_id = request.values.get("chat_id")
        sub = Subscribers.query.filter_by(email=email).first()
        if sub:
            sub.subscribed = True
            sub.number_support_texts = 0
            db.session.commit()

        else:
            subscriber = Subscribers(
                email=email,
                subscribed=True,
                number_support_texts=0,
                platform=platform,
                telegram_chat_id=chat_id,
            )
            db.session.add(subscriber)
            db.session.commit()

        return jsonify(message=f"{email} subscribed successfully")
    except TypeError:
        return jsonify(
            message="There was an error, please try again later or reach out to shapiroj18@gmail.com"
        )


@app.route("/unsubscribedailyjams", methods=["POST"])
def unsubscribedailyjams():
    try:
        email = request.values.get("email").lower()
        platform = request.values.get("platform").lower()

        sub = Subscribers.query.filter_by(email=email).first()
        if sub:
            subs = Subscribers.query.filter_by(email=email)
            for sub in subs:
                sub.subscribed = False
            db.session.commit()
            return jsonify(message=f"{email} removed successfully")
        else:
            return jsonify(message=f"{email} did not exist in the databse")
    except TypeError:
        return jsonify(
            message="There was an error, please try again later or reach out to shapiroj18@gmail.com"
        )


@app.route("/subscribemjm", methods=["POST"])
def subscribemjm():
    try:
        platform = request.values.get("platform").lower()
        chat_id = request.values.get("chat_id")
        sub = MJMAlerts.query.filter_by(telegram_chat_id=chat_id).first()
        if sub:
            sub.mjm_alerts = True
            db.session.commit()

        else:
            mjm_subscriber = MJMAlerts(
                mjm_alerts=True,
                telegram_chat_id=chat_id,
                platform=platform,
            )
            db.session.add(mjm_subscriber)
            db.session.commit()
        return jsonify(message=f"{chat_id} has been subscribed successfully!")

    except TypeError:
        return jsonify(
            message="There was an error, please try again later or reach out to shapiroj18@gmail.com"
        )


@app.route("/unsubscribemjm", methods=["POST"])
def unsubscribemjm():
    try:
        chat_id = request.values.get("chat_id")

        sub = MJMAlerts.query.filter_by(telegram_chat_id=chat_id).first()
        if sub:
            subs = MJMAlerts.query.filter_by(telegram_chat_id=chat_id)
            for sub in subs:
                sub.mjm_alerts = False
                db.session.commit()
            return jsonify(message=f"{chat_id} removed successfully")

        else:
            return jsonify(message=f"{chat_id} did not exist in the databse")

    except TypeError:
        return jsonify(
            message="There was an error, please try again later or reach out to shapiroj18@gmail.com"
        )


@app.route("/randomjam", methods=["GET"])
def get_random_jam():

    song, date = phishnet_api.get_random_jamchart()
    show_info = phishnet_api.get_show_url(date)
    jam_url = phishin_api.get_song_url(song=song, date=date)

    print(song, date, show_info, jam_url)

    return jsonify(
        song=song,
        date=date,
        jam_url=jam_url,
        show_info=show_info,
    )

@app.route("/unsubscribeemail")
def unsubscribeemail():
    return render_template("unsubscribe_email.html")
