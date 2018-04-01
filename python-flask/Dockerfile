# Flask framework

FROM python:alpine3.7

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app.py"]
