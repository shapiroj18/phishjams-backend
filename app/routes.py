import re

from flask import request
from app import app, mail, db
from app.models import Subscribers, MJMAlerts
from app.celery_tasks import send_functions
from flask import render_template
from flask_mail import Message

from twilio.twiml.messaging_response import MessagingResponse


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/radio")
def radio():
    return render_template("radio.html")


@app.route("/email")
def send_mail():
    send_functions.email_send.delay()
    return "Mail Sent"


@app.route("/bot", methods=["POST"])
def bot():
    twilio_post = request.values
    json = twilio_post.to_dict(flat=False)

    incoming_message = request.values.get("Body").lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if incoming_message == "features":
        msg.body(
            f'You can send me messages like:\n"subscribe <email>"\n"unsubscribe <email>"\n"start mjm alerts"\n"stop mjm alerts"\n"code"\nDon\'t worry, more features are coming soon!'
        )

    elif bool(re.match(r"\bsubscribe", incoming_message)):
        email = re.findall(r"\S+@\S+", incoming_message)[0]

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
                platform="Twilio",
                json_response=json,
            )
            db.session.add(subscriber)
            db.session.commit()

        msg.body(f"\U0001F420 {email} has been added for daily random jam emails!")
        responded = True

    elif bool(re.match(r"\bunsubscribe", incoming_message)):
        email = re.findall(r"\S+@\S+", incoming_message)[0]

        subs = Subscribers.query.filter_by(email=email)
        for sub in subs:
            sub.subscribed = False
        db.session.commit()

        msg.body(f"Your email {email} has been unsubscribed from daily jam emails.")
        responded = True

    elif incoming_message == "start mjm alerts":

        sub = MJMAlerts.query.filter_by(phone_number=json["From"][0]).first()
        if sub:
            sub.mjm_alerts = True
            db.session.commit()

        else:
            mjm_subscriber = MJMAlerts(
                mjm_alerts=True,
                phone_number=json["From"][0],
                platform="Twilio",
                json_response=json,
            )
            db.session.add(mjm_subscriber)
            db.session.commit()

        msg.body("You've been subscribed to MJM reminders")
        responded = True

    elif incoming_message == "stop mjm alerts":

        subs = MJMAlerts.query.filter_by(phone_number=json["From"][0])
        for sub in subs:
            sub.mjm_alerts = False
        db.session.commit()
        msg.body(f"You've been unsubscribed from MJM reminders")
        responded = True

    elif incoming_message == "code":
        msg.body(
            f"You can find the source code for this project at github.com/shapiroj18/phish-bot.\nIf you want to contribute, submit a PR or get in contact with shapiroj18@gmail.com!"
        )
        responded = True

    elif not responded:
        msg.body(
            'Not a valid message. Send "features" to see what you can do with this bot'
        )

    return str(resp)
