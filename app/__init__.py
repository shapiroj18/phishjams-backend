import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
from flasgger import Swagger
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv("APP_SETTINGS"))
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
swagger = Swagger(app)
mail = Mail(app)
CORS(app)

from app import routes, models

if __name__ == "__main__":
    app.run
