from phish_bot import db
from sqlalchemy.dialects.postgresql import JSON


class Subscribers(db.Model):
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    subscribed = db.Column(db.Boolean)
    json_response = db.Column(JSON)

    def __repr__(self):
        return f"<id {self.id}"
