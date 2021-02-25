import re
import os
import json

from flask import request, jsonify, render_template, redirect
from app import app, mail, db
from app.models import Subscribers, MJMAlerts
from app.celery_tasks import send_functions
from flask_mail import Message
from app.forms import UnsubscribeEmail

from app.api_tasks import phishnet_api, phishin_api

phishnet_api = phishnet_api.PhishNetAPI()
phishin_api = phishin_api.PhishINAPI()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/japan")
def radio():
    return render_template("japan.html")


@app.route(f"/{os.getenv('RANDOM_VALUE')}/emailtest")
def email():
    return send_functions.email_send_test()


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


@app.route("/randomjam", methods=["POST"])
def get_random_jam():
    try:
        # song = request.values.get("song")
        # year = request.values.get("year")
        
        song=None
        year=1997

        song, date = phishnet_api.get_random_jamchart(song=song, year=year)
        show_info = phishnet_api.get_show_url(date)
        jam_url = phishin_api.get_song_url(song=song, date=date)

        print(song, date, show_info, jam_url)
        
        if "No mp3 for the song" in jam_url:
            return jsonify(response= "No mp3 found for the selected random jam, please try again.")
        else:
            return jsonify(
                song=song,
                date=date,
                jam_url=jam_url,
                show_info=show_info,
            )
    except ValueError:
        return jsonify(response="No jams found for song/year combination")


@app.route("/unsubscribeemail", methods=["Get", "POST"])
def unsubscribeemail():
    form = UnsubscribeEmail()
    if form.validate_on_submit():
        email = form.email.data

        subs = Subscribers.query.filter_by(email=email)
        for sub in subs:
            sub.subscribed = False
        db.session.commit()
        return redirect("/successfulunsubscribe")

    return render_template("unsubscribe_email.html", form=form)


@app.route("/successfulunsubscribe")
def successfulunsubscribe():
    return render_template("successful_unsubscribe.html")


@app.route("/get_song_info", methods=["GET"])
def get_song_info():

    mock_db = [
        {
            "name": "Shafty",
            "artist": "Phish",
            "url": "https://phish.in/audio/000/018/032/18032.mp3",
            "cover_art_url": "static/img/livephish_logos/1998-04-05.jpg",
            "date": "1998-04-05",
        },
        {
            "name": "Divided Sky",
            "artist": "Phish",
            "url": "https://phish.in/audio/000/031/902/31902.mp3",
            "cover_art_url": "static/img/livephish_logos/1987-05-11.jpg",
            "date": "1987-05-11",
        },
    ]

    songs = json.dumps(mock_db)

    return jsonify(songs)
