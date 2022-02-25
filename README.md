[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Phish Bot

This is a bot that can send you random jams, reminders for mystery jam monday and play your favorite jams!

Info:
Telegram -
  * Prod - `@gone_phishing_bot`
  * Dev - `@dev_gone_phishing_bot`
  * Local - `@devlocal_gone_phishing_bot`

Web App -
  * Prod - `https://phishjams.herokuapp.com/`
  * Dev - `https://phishjams-dev.herokuapp.com/`
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
* [Flasgger](https://github.com/flasgger/flasgger)
* [Counter](https://counter.dev/) (website statistics)
* [GitHub Actions](https://docs.github.com/en/actions)

Development:
* Environmental variables are stored in the `.env.template`. You should copy that to your environment as `.env` and fill in the required variables.
* Confirm Docker is running on your machine `docker info` and ports are cleared (`docker ps`)
* Run `source start-dev-env.sh` to do the following:
  * Start virtual environment
  * Log in to heroku
  * Start ngrok proxy at port 8443 locally
  * Start `docker-compose` 
* Then you will be able to:
  * Access the web server at `http://localhost:5000/`
  * Access API docs at `http://localhost:5000/apidocs`
  * Access flower at `http://localhost:5555/`
  * Access ngrok at `http://localhost:4040/`
  * Access posgres via `docker exec` or a database client. If using a database client, make sure to show all databases to see `phishbot_local_dev`. For example, in DBeaver, when adding a new posgres database, go to the `PostgreSQL` tab and select `Show all databases`. Once the connection has been created, make sure the correct database is selected by right clicking and choosing "Set as default."

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
* There is an ad-hoc script for seeing which album covers by show date are missing. In order to run it:
1. Open the root of this project
2. If you have a virtual environment already started with this project, just make sure that is activated. Otherwise, start a new one and `pip install -r requirements.txt`. It also accesses Phish.Net's API, so make sure your `.env` file is has that token (see environmental variables above).
3. `cd app/scripts`
4. `python check_cover_art_diff.py` 

This will print the shows missing from `/app/static/img/livephish_logos` to `stdout`.

## Contributing:
Very much encouraged! Simply submit a PR or reach out to shapiroj18@gmail.com.

Find my profile on [phish.net](https://phish.net/user/harpua18)!
