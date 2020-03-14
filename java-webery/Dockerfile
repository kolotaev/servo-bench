# build
FROM gradle:5.4.1-jdk11 as gradle

USER root
WORKDIR /app

COPY build.gradle build.gradle
COPY src src

RUN gradle clean fatJar

# prod
FROM openjdk:11.0.3-jdk-slim
WORKDIR /app
COPY --from=gradle /app/build/libs/benchy-server-all-1.0-SNAPSHOT.jar app.jar
CMD ["java", "-server", "-jar", "app.jar", "env=prod"]
