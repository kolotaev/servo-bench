# Clojure Ring library/framework

FROM clojure:alpine

ADD . .

RUN lein deps

RUN lein uberjar

EXPOSE 8080

CMD ["java", "-jar", "target/serv-0.0.1-standalone.jar"]
