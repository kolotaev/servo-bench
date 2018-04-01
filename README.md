# Benchmark of various web-frameworks

> Tests for machines with limited resources (1 vCPU, 512 Mb RAM).

- [Frameworks](#frameworks)
  - [Go. Echo.](#go-echo)
  - [JS. Express.](#js-express)
  - [Python. Flask.](#python-flask)
- [Mule script](#mule-scrip)
- [Results](#results)


## Frameworks

Every framework section has 2 words: Language. Framework name.

### Go. Echo.

- [Site](https://github.com/labstack/echo)


Logging enabled? - false


*JSON*

> %CPU %MEM

> 94.9  2.4

> running: 361mb used

> before launch: 350mb used

```
wrk -t12 -c400 -d300s http://lamp:8080/json
Running 5m test @ http://lamp:8080/json
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    27.74ms   27.79ms 235.84ms   76.27%
    Req/Sec   725.22    369.98     2.17k    51.94%
  2596838 requests in 5.00m, 500.26MB read
  Socket errors: connect 156, read 0, write 0, timeout 0
Requests/sec:   8653.99
Transfer/sec:      1.67MB
```

DB
?

```
wrk -t12 -c400 -d300s http://lamp:8080/db
Running 5m test @ http://lamp:8080/db
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.65s   306.46ms   2.00s    76.23%
    Req/Sec     8.52      6.74    60.00     76.87%
  21299 requests in 5.00m, 7.59GB read
  Socket errors: connect 156, read 0, write 0, timeout 18758
Requests/sec:     70.98
Transfer/sec:     25.89MB
```


### JS. Express.

- [NodeJS site](nodejs.org)
- [Express site](https://expressjs.com)


### Python. Flask.

- [Site](http://flask.pocoo.org)


## Mule script

`mule`is a script to help you build and run specific framework in a docker-container.

Script can be run by 2 possible ways:

```bash
# 1. From repo's root directory: you need to specify directory of the framework in -d option.
./mule.sh -d go-echo

# 2. From specific framework's directory: no -d option is needed.
cd go-echo
../mule.sh
```

Available actions of using `mule` (assuming the 2nd way of running):

- Read help for `mule` script
```bash
../mule.sh -h
```

- Build/rebuild image
```bash
../mule.sh -b
```

- Run container
```bash
../mule.sh -r
```

- Run container with attached TTY (to see its output)
```bash
../mule.sh -ra
```

- Kill running container
```bash
../mule.sh -k
```

- Build image, kill container if running, run new w/ attached TTY
```bash
../mule.sh -brak
```

- Run with specific options (port, loop-count, etc.)
```bash
../mule.sh -ra -p 8088 -l 1000
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
