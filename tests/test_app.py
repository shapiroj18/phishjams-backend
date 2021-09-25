import os
import sys
import tempfile
import pytest

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import app


@pytest.fixture
def client():
    db_fd, app.app.config["DATABASE"] = tempfile.mkstemp()
    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.app.config["DATABASE"])