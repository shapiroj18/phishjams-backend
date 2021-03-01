import re
import os
import json

from flask import request, jsonify, render_template, redirect
from app import app, mail, db
from app.models import Subscribers, MJMAlerts, PhishJamsQueue
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
        song = request.values.get("song")

        song, date = phishnet_api.get_random_jamchart(song=song)
        show_info = phishnet_api.get_show_url(date)
        jam_url = phishin_api.get_song_url(song=song, date=date)

        print(song, date, show_info, jam_url)

        if "No mp3 for the song" in jam_url:
            return jsonify(
                song=song,
                date=date,
                jam_url=None,
                show_info=show_info,
            )
        else:
            return jsonify(
                song=song,
                date=date,
                jam_url=jam_url,
                show_info=show_info,
            )
    except (ValueError, UnboundLocalError) as e:
        print(f"Error: {e}")
        return jsonify(response="No jams found for that song. Please try again!")


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


@app.route("/addtoqueue", methods=["POST"])
def add_to_queue():
    try:
        song = request.values.get("song") 
        date = request.values.get("jam_date")

        if song and date:
            show_info = phishnet_api.get_show_url(date)
            jam_url = phishin_api.get_song_url(song=song, date=date)
            print(song, date, show_info, jam_url)
            
        else:
            song, date = phishnet_api.get_random_jamchart(song=song)
            show_info = phishnet_api.get_show_url(date)
            jam_url = phishin_api.get_song_url(song=song, date=date)
            print(song, date, show_info, jam_url)

        if "No mp3 for the song" in jam_url:
            return jsonify(
                song=song,
                date=date,
                jam_url=None,
                show_info=show_info,
            )
        else:

            dir_path = os.path.dirname(os.path.realpath(__file__))
            cover_art_file = f"static/img/livephish_logos/{date}.jpg"
            path_cover_art = os.path.join(dir_path, cover_art_file)
            if os.path.exists(path_cover_art):
                cover_art_url = cover_art_file
            else:
                cover_art_url = os.path.join(
                    dir_path, "static/img/livephish_logos/default.jpg"
                )

            queue_item = PhishJamsQueue(
                telegram_chat_id=request.values.get("chat_id"),
                platform=request.values.get("platform"),
                user_first_name=request.values.get("user_first_name"),
                song_name=song,
                song_url=jam_url,
                cover_art_url=cover_art_url,
                show_date=date,
            )

            db.session.add(queue_item)
            db.session.commit()

            return jsonify(
                song=song,
                date=date,
                jam_url=jam_url,
                show_info=show_info,
            )
    except (ValueError, UnboundLocalError, IndexError) as e:
        print(f"Error: {e}")
        return jsonify(response="No jams found for that song. Please try again!")


@app.route("/get_song_info", methods=["GET"])
def get_song_info():

    songs = []
    queue_songs = PhishJamsQueue.query.all()
    for song in queue_songs:
        song_obj = {
            "name": song.song_name,
            "artist": "Phish",
            "url": song.song_url,
            "cover_art_url": song.cover_art_url,
            "date": song.show_date,
        }
        songs.append(song_obj)

    songs_obj = json.dumps(songs)

    return jsonify(songs_obj)
