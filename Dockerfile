FROM python:3.9-slim-buster
WORKDIR /usr/src/app
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000