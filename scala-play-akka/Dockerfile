# Play framework

FROM frolvlad/alpine-oraclejdk8

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY test-app .

RUN sbt
RUN sbt dist
RUN unzip target/universal/test-app-1.0.zip && chmod +x test-app-1.0/bin/test-app

EXPOSE 9000 8080

CMD ["test-app-1.0/bin/test-app", "-Dplay.http.secret.key=abcdefghijk", "-Dconfig.file=/usr/src/app/conf/application.conf"]
