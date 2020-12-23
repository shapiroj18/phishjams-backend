import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import result


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def helloname(name):
    return f"Hello, {name}"


if __name__ == "__main__":
    app.run
