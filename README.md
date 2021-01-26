[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Phish Bot

The bot is called `@gone_phishing_bot` on Telegram

Deployed at `https://phish-telegram-bot.herokuapp.com/`

Commands:
Simply type `/` into Telegram when you are chatting with the bot or read `main()` of   `app.py`

Notes:
Environmental variables are stored as [heroku config vars](https://devcenter.heroku.com/articles/config-vars)

Technologies:
* Flask
* PostgreSQL
* Celery
* Redis
* Autoenv
* Flask-Mail
* Flask-Migrate
* Ngrok for local testing

Development:
* You need [Python3](https://www.python.org/downloads/) and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) installed.
* Run `source start-dev-env.sh` to do the following:
  * Start virtual environment
  * Log in to heroku
  * Store local env variables
  * Start postgres
* Run `docker-compose up --build` to start the web server, celery, flower and redis.
  * Access web server at `http://0.0.0.0:5000/`
  * Access flower at `http://localhost:5555/`
* You need to start `ngrok` for a local environment. Download from the [website](https://ngrok.com/download) and follow their instructions for getting started. Then run `ngrok http 5000` and copy and paste the https url as a webhook to Twilio, etc (make sure route is included in webhook url)
* Start celery locally with `celery -A app.celery_tasks.celery worker --loglevel=INFO` once you have installed redis (`brew install redis`) and started `redis-server`. You can check if the redis server is running with `redis-cli ping` (you should get back `PONG`). Start celery beat locally with `celery -A app.celery_tasks.celery beat --loglevel=INFO`. You can start both the celery worker and beat with `celery worker -A app.celery_tasks.celery --beat --loglevel=info`. Run `flower` with `flower -A app.celery_tasks.celery --port=5555`
* Postgres can be installed and run via [this page](https://wiki.postgresql.org/wiki/Homebrew). Make sure your databases are defined in your `.env`.
  * `psql postgres`
  * `CREATE DATABASE phishbot_local_dev;`
  * `\c phishbot_local_dev`
  * `\du` to list users
  * `ALTER USER <username> WITH PASSWORD '<password>';`
  * Connect to postgres with host: `localhost`, port: `5432`, database: `phishbot_local_dev`, username: `username` and password: `password`
  * See tables with `\dt`
  * Add `DATABASE_URL=postgresql:///phishbot_local_dev` to your `.env`
  * `flask db upgrade` to update database with flask models. If this isn't working make sure your `.env` is being imported via `dotenv`.

The environmental variables stored are:
1. BOT_TOKEN=`bot_token` (token for `@gone_phishing_bot` from BotFather)
2. BOT_USERNAME=`username` (username for `@gone_phishing_bot` from BotFather)
3. URL=`url` (url of heroku app)
4. PHISHNET_API_KEY=`api_key` (API Key for Phish.Net, [retrieved here](https://api.phish.net/request-key))
5. PHISHIN_API_KEY=`api_key` (API Key for Phish.in can be requested at the [contacts page](https://phish.in/contact-info) and info about the api can be found in the [api docs](https://phish.in/api-docs))

To Do:
1. Make sure json responses for required functions are not more than one page with if/else
2. Pytest
3. Mypy
4. Phish Trivia Game
5.  Automatically send mjm when it gets posted
6.  Build Dev Env
    * Create all functionality except the run in one file
    * Create `start.logging()` for with dev bot for dev env
    * Create `set_webhook()` for CI/CD with full bot for when I push
7.  Figure out how to automate `flask db upgrade`
8.  Tests and incorporate into github actions
9.  Add email template and phish radio template (when people request ping to a cool-looking graph?) https://ron.sh/creating-real-time-charts-with-flask/
10. Create events tables (when messages are sent, when messages are received)
11. Sponsorship messages 1/week
12. Better unsubscribe messaging