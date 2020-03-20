# build
FROM gradle:4.6 as gradle

USER root
WORKDIR /app

COPY build.gradle build.gradle
COPY src src

RUN gradle clean shadowJar
RUN ls -la /app/build/libs/

# prod
FROM openjdk:11.0.3-jdk-slim
WORKDIR /app
COPY --from=gradle /app/build/libs/app-0.1.0-SNAPSHOT-fat.jar app.jar
CMD ["java", "-server", "-jar", "app.jar", "env=prod"]
