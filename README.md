# Benchmark various web-frameworks for machines with limited resources

- [Frameworks](#frameworks)
  - [Go. Echo.](#go-echo)
- [Build image](#build)
- [Run](#run)
- [Results](#results)


## Frameworks

### Go. Echo.

[Page](https://github.com/labstack/echo)


## Build

```bash
cd WEB_FRAMEWORK_FOLDER
../build.sh
```

## Run

```bash
./run.sh -i FRAMEWORK_NAME -d DETACHED_OR_NOT(yes/no)
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
