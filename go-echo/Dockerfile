# Go Echo framework

FROM golang:1.15-alpine

WORKDIR /server
RUN apk add --no-cache git

ADD . .
RUN go mod vendor
RUN go build server.go && mv server goecho

ENTRYPOINT ./runner.sh
EXPOSE 8080
