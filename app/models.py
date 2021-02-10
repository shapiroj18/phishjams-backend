from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Subscribers(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    subscribed = db.Column(db.Boolean)
    platform = db.Column(db.String(60))
    number_support_texts = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    telegram_chat_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<id {self.id}>"


class MJMAlerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mjm_alerts = db.Column(db.Boolean)
    platform = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    telegram_chat_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<id {self.id}>"


# class EmailSends(db.Model):
