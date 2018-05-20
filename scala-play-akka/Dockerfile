# Play framework

FROM iflavoursbv/sbt-openjdk-8-alpine

# Create app directory
WORKDIR /usr/src/app

# Add project dependencies
COPY application/build.sbt ./build.sbt
COPY application/project ./project
RUN sbt update

# Bundle app source
COPY application .

# Create production executable
RUN sbt dist && unzip target/universal/application-1.0.zip && chmod +x application-1.0/bin/application

EXPOSE 8080

CMD ["application-1.0/bin/application", "-Dplay.http.secret.key=abcdefghijk", "-Dconfig.file=/usr/src/app/conf/application.conf"]
