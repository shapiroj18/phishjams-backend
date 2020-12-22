# Phish Bot

Flask App
Dev / Prod
- Local Development (localhost with dev variables - twilio dev number)
- GitHub - (main and stage branch) (push to two diff heroku apps)
- Heroku App (main app and stage app) (heroku postgres for each prod and stage) (pipelines are a good idea)
- Twilio - (main number and dev number)
Flask Architecture
- Views to connect to telegram
- Views to connect to twilio
- Database
- Config.py / .env file: local, stage, prod
- Look up what another website structured flask or how Django does it