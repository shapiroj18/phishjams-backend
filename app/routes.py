from app import app, mail
from flask_mail import Mail, Message
from app import phishnet_api, phishin_api

phishnet_api = phishnet_api.PhishNetAPI()
phishin_api = phishin_api.PhishINAPI()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def helloname(name):
    return f"Hello, {name}"


@app.route("/emailtest")
def emailtest():
    song, date = phishnet_api.get_random_jamchart()

    with app.app_context():
        msg = Message(
            subject="Phish Test",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=["shapiroj18@gmail.com"],
            body="Show Link (Phish.in)", url=f"https://phish.in/{date}",
        )
        mail.send(msg)

    return "Mail Sent"
