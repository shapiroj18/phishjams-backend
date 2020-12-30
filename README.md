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

Development:
* You need [Python3](https://www.python.org/downloads/) and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) installed.
* Run `source start-dev-env.sh` to start virtual environment, log in to heroku and store local env variables. Include a Phishy surprise with `-p` or `--phish`.
* Start celery locally with `celery -A app.tasks.celery worker --loglevel=INFO` once you have `brew install redis` and started `redis-server`. You can check if the redis server is running with `redis-cli ping` (you should get back `PONG`)

The environmental variables stored are:
1. BOT_TOKEN=`bot_token` (token for `@gone_phishing_bot` from BotFather)
2. BOT_USERNAME=`username` (username for `@gone_phishing_bot` from BotFather)
3. URL=`url` (url of heroku app)
4. PHISHNET_API_KEY=`api_key` (API Key for Phish.Net, [retrieved here](https://api.phish.net/request-key))
5. PHISHIN_API_KEY=`api_key` (API Key for Phish.in can be requested at the [contacts page](https://phish.in/contact-info) and info about the api can be found in the [api docs](https://phish.in/api-docs))

To Do:
1. Make sure json responses for required functions are not more than one page with if/else
2. Set option for only soundboards?
3. Make date format acceptance broader than just YYYY-MM-DD
4. Pytest
5. Mypy
6. Phish Trivia Game!
7. Create md file for commands
8.  Automatically send mjm when it gets posted
9.  CI/CD
10. See if pushing new build removes all previous jobs
11. Httpx instead of Requests
12. Build Dev Env
    * Create all functionality except the run in one file
    * Create `start.logging()` for with dev bot for dev env
    * Create `set_webhook()` for CI/CD with full bot for when I push
13. Figure out how to automate `flask db upgrade`
14. Blueprints
15. Tests and incorporate into github actions
16. Readme or badges for technologies (diagram?):
    - heroku
    - dotenv
    - Postgres
    - celery/rabbitmq
17. Add email template and phish radio template (when people request ping to a cool-looking graph?) https://ron.sh/creating-real-time-charts-with-flask/
18. Dockerize