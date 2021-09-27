[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Phish Bot

This is a bot that can send you random jams, reminders for mystery jam monday and play your favorite jams!

Info:
Telegram -
  * Prod - `@gone_phishing_bot`
  * Dev - `@dev_gone_phishing_bot`
  * Local - `@devlocal_gone_phishing_bot`

Web App -
  * Prod - `https://phishjam-bot.herokuapp.com/`
  * Dev - `https://phishjam-bot-dev.herokuapp.com/`
  * Local - Uses `ngrok` and local server (see below)

Server - 
Uses Heroku for Prod and Dev deployments. Uses [cron-job.org](https://cron-job.org/en/) to send API calls such that the server wakes up for celery jobs.

Contributing:
Very much encouraged! Simply submit a PR or reach out to shapiroj18@gmail.com.

### Notes:
Environmental variables are stored as [heroku config vars](https://devcenter.heroku.com/articles/config-vars)

Technologies:
* Flask
* PostgreSQL
* Celery / Flower
* Redis
* Flask-Mail with Sendgrid
* Flask-Migrate
* Ngrok
* https://counter.dev/ (website statistics)

Development:
* Run `source start-dev-env.sh` to do the following:
  * Start virtual environment
  * Log in to heroku
  * Store local env variables
* Make sure docker is running and then run `docker-compose up --build --remove-orphans` to start local microservices. Note that `ngrok` only lasts two hours without an account so you will have to rerun `docker-compose up` once that time limit is up.
  * Access web server at `http://localhost:5000/`
  * Access flower at `http://localhost:5555/`
  * Access ngrok at `http://localhost:4040/`
  * Access posgres via `docker exec` or a database client. If using a database client, make sure to show all databases to see `phishbot_local_dev`. For example, in DBeaver, when adding a new posgres database, go to the `PostgreSQL` tab and select `Show all databases`.

Dependencies:
* [Python3](https://www.python.org/downloads/)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

The environmental variables stored are:
1. BOT_TOKEN=`bot_token` (token for `@gone_phishing_bot` from BotFather)
2. BOT_USERNAME=`username` (username for `@gone_phishing_bot` from BotFather)
3. URL=`url` (url of heroku app)
4. PHISHNET_API_KEY=`api_key` (API Key for Phish.Net, [retrieved here](https://api.phish.net/request-key))
5. PHISHIN_API_KEY=`api_key` (API Key for Phish.in can be requested at the [contacts page](https://phish.in/contact-info) and info about the api can be found in the [api docs](https://phish.in/api-docs))

Find my profile on [phish.net](https://phish.net/user/harpua18)!