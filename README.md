# Benchmark of various web-frameworks

> Tests for minimal machines with limited resources (1 vCPU, 1 Gb RAM).

- [Frameworks](#frameworks)
  - [Go. Echo.](#go-echo)
  - [JS. Express.](#js-express)
  - [Python. Flask. Gevent.](#python-flask-gevent)
  - [Python. Aiohttp. UVloop.](#python-aiohttp)
  - [Clojure. Ring. Jetty.](#clojure-ring-jetty)
  - [Scala. Play. Akka.](#scala-play-akka)
  - [Elixir. Phoenix. OTP.](#elixir-phoenix-otp)
- [Mule script](#mule-script)
- [Runner script](#runner-script)
- [Results](#results)


## Frameworks

Every framework section has 2 (or 3) words: Language. Framework name. (Web server name or networking library)

### Go. Echo.

- [Echo](https://github.com/labstack/echo)

Logging enabled? - false


### JS. Express.

- [NodeJS site](nodejs.org)
- [Express site](https://expressjs.com)


### Python. Flask. Gevent

- [Flask](http://flask.pocoo.org)
- [Gunicorn](http://gunicorn.org/#docs)
- [Gevent](http://www.gevent.org)

With setup: 'Gunicorn as a web-server. 4 workers. Worker type - async: eventlet' server gives only 3-4 req/s
which is very low.

Tuned bare gevent is much better.


### Python. Aiohttp. UVloop.

- [Aiohttp](https://aiohttp.readthedocs.io/en/stable/index.html)
- [uvloop](https://github.com/MagicStack/uvloop)
- [acyncpg](https://magicstack.github.io/asyncpg)

Strange, but UVloop gives no benefits for `db/` endpoint.


### Clojure. Ring. Jetty.

- [Ring](https://github.com/ring-clojure/ring)
- [Jetty](https://www.eclipse.org/jetty)

Jetty with all default settings.


### Scala. Play. Akka.

- [Play](https://www.playframework.com)
- [Akka](https://akka.io)


### Elixir. Phoenix. OTP.

- [Elixir](https://elixir-lang.org)
- [Phoenix](https://phoenixframework.org)
- [Erlang & OTP](https://www.erlang.org)


### Elixir. Plug. OTP.

- [Elixir](https://elixir-lang.org)
- [Plug](https://github.com/elixir-plug/plug)
- [Erlang & OTP](https://www.erlang.org)


### Ruby. Sinatra. Synchrony.

- [Ruby](https://www.ruby-lang.org)
- [Sinatra](http://sinatrarb.com)
- [Synchrony](https://github.com/kyledrake/sinatra-synchrony)


## Mule script

`mule` is a script to help you build and run specific framework in a docker-container.

Script can be run in 2 possible ways:

```bash
# 1. From repo's root directory: you need to specify directory of the framework in -d option.
./mule.sh -d go-echo

# 2. From specific framework's directory: no -d option is needed.
cd go-echo
../mule.sh
```

Available actions of using `mule` (assuming the 2nd way of running):

```bash
# Read help for `mule` script
../mule.sh -h

# Build all images
./mule.sh -x

# Build/rebuild image
../mule.sh -b

# Run container
../mule.sh -r

# Run container with attached TTY (to see its output)
../mule.sh -ra

# Kill running container
../mule.sh -k

# Build image, kill container if running, run new w/ attached TTY
../mule.sh -brak

# Run with specific options (loop-count, etc.)
../mule.sh -ra -l 1000
```


## Results

Simple random JSON response.

For

```
wrk -t12 -c400 -d300s http://vagrant-machine:8080/json
```

Postgres DB call that does `sleep random(2 sec)`.

For

```
wrk -t12 -c400 -d300s http://vagrant-machine:8080/db
```
