from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Subscribers(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    subscribed = db.Column(db.Boolean)
    platform = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    json_response = db.Column(JSON)

    def __repr__(self):
        return f"<id {self.id}>"
