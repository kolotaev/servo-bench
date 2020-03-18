FROM maven:3.6.1-jdk-11-slim as maven
WORKDIR /vertx
COPY src src
COPY pom.xml pom.xml
RUN mvn package -q
CMD ["java", "-server", "-jar", "target/vertx.benchmark-0.0.1-SNAPSHOT-fat.jar", "src/main/conf/config.json"]
