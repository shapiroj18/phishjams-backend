import os
from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS"))

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def helloname(name):
    return f"Hello, {name}"


if __name__ == "__main__":
    app.run
