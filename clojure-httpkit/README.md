### Test remote with http-kit-client async.

The golang db server itself with sleep 2:

```
wrk -t12 -c400 -d240s http://localhost:8081/db --timeout 10s --latency
Running 4m test @ http://localhost:8081/db
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.17s   608.28ms   2.92s    60.28%
    Req/Sec    19.74     14.56    99.00     71.04%
  Latency Distribution
     50%    1.19s 
     75%    1.67s 
     90%    1.97s 
     99%    2.38s 
  12844 requests in 1.14m, 472.08MB read
  Socket errors: connect 156, read 730, write 0, timeout 0
Requests/sec:    188.09
Transfer/sec:      6.91MB
```

The remote call via http client from clojure (no data looping):

```
wrk -t12 -c400 -d240s http://localhost:8080/remote --timeout 10s --latency
Running 4m test @ http://localhost:8080/remote
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.16s   602.66ms   2.95s    59.79%
    Req/Sec    20.60     16.25   145.00     67.51%
  Latency Distribution
     50%    1.15s 
     75%    1.67s 
     90%    1.97s 
     99%    2.34s 
  11025 requests in 0.98m, 1.40MB read
  Socket errors: connect 156, read 695, write 1, timeout 0
Requests/sec:    188.12
Transfer/sec:     24.43KB
```