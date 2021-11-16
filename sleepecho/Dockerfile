# Sleeping echo server

FROM golang:1.13-alpine
ADD server.go sleepecho.go
RUN go build sleepecho.go
ENTRYPOINT ./sleepecho
EXPOSE 9000
