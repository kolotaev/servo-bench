# Benchmark various web-frameworks

> Tests done for machines with limited resources

- [Frameworks](#frameworks)
  - [Go. Echo.](#go-echo)
- [Build image](#build-image)
- [Run image](#run-image)
- [Kill image](#kill-image)
- [Results](#results)


## Frameworks

### Go. Echo.

[Page](https://github.com/labstack/echo)

%CPU %MEM
94.9  2.4

mem 361556 used ut of 352000

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


## Build image

```bash
cd WEB_FRAMEWORK_FOLDER
../build.sh
```

## Run image

```bash
./run.sh -i FRAMEWORK_NAME -d DETACHED_OR_NOT(yes/no) -p PORT

or

cd WEB_FRAMEWORK_FOLDER
../run.sh
```

## Kill image

```bash
cd WEB_FRAMEWORK_FOLDER
../kill.sh

or

./kill.sh WEB_FRAMEWORK_FOLDER
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
