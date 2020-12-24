from app import app


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def helloname(name):
    return f"Hello, {name}"
