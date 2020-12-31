import re

from flask import request
from app import app, mail, db
from app.models import Subscribers
from app.celery_tasks import timed_functions, send_functions
from flask import render_template
from flask_mail import Message

from twilio.twiml.messaging_response import MessagingResponse


@app.route("/")
def hello():
    return "Listen to the Japan 2000 Tour"


@app.route("/radio")
def radio():
    return f"Phish Radio"


@app.route("/process/<name>")
def process(name):
    timed_functions.reverse.delay(name)
    return "Async sent"


@app.route("/emailtest")
def emailtest():
    send_functions.daily_email_sends()
    return "Mail sent"


@app.route("/bot", methods=["POST"])
def bot():
    twilio_post = request.values
    json = twilio_post.to_dict(flat=False)

    incoming_message = request.values.get("Body").lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if bool(re.match(r"\bsubscribe", incoming_message)):
        email = re.findall("\S+@\S+", incoming_message)[0]
        subscriber = Subscribers(
            email=email, subscribed=True, platform="Twilio", json_response=json
        )
        db.session.add(subscriber)
        db.session.commit()
        msg.body(f"\U0001F420 {email} has been added for daily random jam emails!")
        responded = True

    elif bool(re.match(r"\bunsubscribe", incoming_message)):
        email = re.findall("\S+@\S+", incoming_message)[0]

        subs = Subscribers.query.filter_by(email=email)
        for sub in subs:
            sub.subscribed = False

        db.session.commit()

        msg.body(f"Your email {email} has been unsubscribed from daily jam emails.")
        responded = True
    elif not responded:
        msg.body('Not a valid message. Send "subscribe <email>" or "unsubscribe <email>"')

    return str(resp)
