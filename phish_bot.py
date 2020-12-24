from app import app, db
from app.models import Subscribers


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Subscribers": Subscribers}
