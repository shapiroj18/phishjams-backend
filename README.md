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
  * Local - Uses `ngrok` and local server (established as a part of the dev startup script)

Server - 
Uses Heroku for Prod and Dev deployments. Uses [cron-job.org](https://cron-job.org/en/) to send API calls such that the server wakes up for celery jobs.

### Notes:
Environmental variables are stored as [heroku config vars](https://devcenter.heroku.com/articles/config-vars)

Technologies:
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [PostgreSQL](https://www.postgresql.org/)
* [Celery](https://docs.celeryproject.org/en/stable/index.html) / [Flower](https://flower.readthedocs.io/en/latest/)
* [Redis](https://redis.io/)
* [Heroku](https://heroku.com)
* [Ngrok](https://ngrok.com/)
* [Flask-Mail](https://pythonhosted.org/Flask-Mail/) / [Sendgrid](https://sendgrid.com/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Counter](https://counter.dev/) (website statistics)

Development:
* Environmental variables are stored in teh `.env.template`. You should copy that to your environment as `.env` and fill in the required variables.
* Run `source start-dev-env.sh` to do the following:
  * Start virtual environment
  * Log in to heroku
  * Start ngrok proxy at port 8443 locally
  * Start `docker-compose` 
* Then you will be able to:
  * Access the web server at `http://localhost:5000/`
  * Access flower at `http://localhost:5555/`
  * Access ngrok at `http://localhost:4040/`
  * Access posgres via `docker exec` or a database client. If using a database client, make sure to show all databases to see `phishbot_local_dev`. For example, in DBeaver, when adding a new posgres database, go to the `PostgreSQL` tab and select `Show all databases`.

Dependencies:
* [Python3](https://www.python.org/downloads/)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
* [Ngrok](https://ngrok.com/download)

The environmental variables stored are:
1. BOT_TOKEN=`bot_token` (token for `@gone_phishing_bot` from BotFather)
2. BOT_USERNAME=`username` (username for `@gone_phishing_bot` from BotFather)
3. URL=`url` (url of heroku app)
4. PHISHNET_API_KEY=`api_key` (API Key for Phish.Net, [retrieved here](https://api.phish.net/request-key))
5. PHISHIN_API_KEY=`api_key` (API Key for Phish.in can be requested at the [contacts page](https://phish.in/contact-info) and info about the api can be found in the [api docs](https://phish.in/api-docs))

Additional Notes:
* Migration scripts (Flask-Migrate) should be generated against the docker container that is running postgres:
  ```
  docker-compose exec web flask db migrate -m '<migration message>'
  ``` 

## Contributing:
Very much encouraged! Simply submit a PR or reach out to shapiroj18@gmail.com.

Find my profile on [phish.net](https://phish.net/user/harpua18)!