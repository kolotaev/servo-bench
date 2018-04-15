# Clojure Ring library/framework

FROM clojure:alpine

ADD . .

RUN lein uberjar

ENTRYPOINT "java -jar target/serv-0.0.1-standalone.jar"

EXPOSE 8080
