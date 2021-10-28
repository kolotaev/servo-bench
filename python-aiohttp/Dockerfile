# Aiohttp framework

FROM python:alpine3.7 AS python_aiohttp_build
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add make
# Create app directory
WORKDIR /usr/src/app
# Bundle dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


FROM python_aiohttp_build
COPY server.py server.py
EXPOSE 8080
CMD ["python", "server.py"]
