# Flask framework

FROM python:alpine3.7

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["gunicorn", "--config", "gunicorn_config.py", "server:app"]
