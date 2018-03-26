# Go Echo framework

FROM golang:alpine

RUN apk add --no-cache git

RUN go get -u github.com/labstack/echo/... && go get github.com/lib/pq/...

ADD . .

RUN go build server.go

ENTRYPOINT ./server

EXPOSE 8080
