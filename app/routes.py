from app import app, mail
from flask_mail import Mail, Message


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def helloname(name):
    return f"Hello, {name}"


@app.route("/emailtest")
def emailtest():

    with app.app_context():
        msg = Message(
            subject="Phishing Test",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=["shapiroj18@gmail.com"],
            body="Phish Jams Go Here",
        )
        mail.send(msg)

    return "Mail Sent"
