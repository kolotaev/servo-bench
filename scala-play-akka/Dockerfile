# Play framework

FROM frolvlad/alpine-oraclejdk8

# Create app directory
WORKDIR /usr/src/app

# Bundle app source
COPY application .

RUN sbt update
RUN sbt dist
RUN unzip target/universal/application-1.0.zip && chmod +x application-1.0/bin/application

EXPOSE 9000 8080

CMD ["application-1.0/bin/application", "-Dplay.http.secret.key=abcdefghijk", "-Dconfig.file=/usr/src/app/conf/application.conf"]
