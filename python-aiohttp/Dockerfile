# Aiohttp framework

FROM python:alpine3.6

RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add make

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "server.py"]
