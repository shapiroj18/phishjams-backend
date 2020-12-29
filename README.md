[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Phish Bot

The bot is called `@gone_phishing_bot`

Deployed at `https://phish-telegram-bot.herokuapp.com/`

Commands:
Simply type `/` into Telegram when you are chatting with the bot or read `main()` of   `app.py`

Notes:
Environmental variables are stored as [heroku config vars](https://devcenter.heroku.com/articles/config-vars)

Development:
* You need [Python3](https://www.python.org/downloads/) and the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) installed.
* Run `source start-dev-env.sh` to start virtual environment, log in to heroku and store local env variables. Include a Phishy surprise with `-p` or `--phish`.

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
9.  Get email updates
10. CI/CD
11. See if pushing new build removes all previous jobs
12. Httpx instead of Requests
13. Build Dev Env
    * Create all functionality except the run in one file
    * Create `start.logging()` for with dev bot for dev env
    * Create `set_webhook()` for CI/CD with full bot for when I push
14. Figure out how to automate `flask db upgrade`
15. Blueprints
16. Celery
17. Tests and incorporate into github actions
18. Readme or badges for technologies (diagram?):
    - heroku
    - dotenv
    - Postgres
    - celery/rabbitmq
19. Get local and dev phishin keys


Flask App
Dev / Prod
- Local Development (localhost with dev variables - twilio dev number)
- GitHub - (main and stage branch) (push to two diff heroku apps)
- Heroku App (main app and stage app) (heroku postgres for each prod and stage) (pipelines are a good idea)
- Twilio - (main number and dev number and local number)
Flask Architecture
- Views to connect to telegram
- Views to connect to twilio
- Database
- Config.py / .env file: local, stage, prod
- Look up what another website structured flask or how Django does it