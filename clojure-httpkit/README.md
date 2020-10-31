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


With vectorized rand string:

DB sleep 0.

Golang baseline:
```
wrk -t12 -c400 -d240s http://localhost:8081/db --timeout 10s --latency
Running 4m test @ http://localhost:8081/db
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.07s   553.61ms   2.95s    62.61%
    Req/Sec    23.54     15.82   111.00     74.20%
  Latency Distribution
     50%  963.74ms
     75%    1.56s 
     90%    1.81s 
     99%    2.15s 
  27954 requests in 2.18m, 1.00GB read
  Socket errors: connect 156, read 726, write 1, timeout 0
Requests/sec:    214.04
Transfer/sec:      7.87MB
```

Clojure:

```
wrk -t12 -c400 -d240s http://localhost:8080/remote --timeout 10s --latency
Running 4m test @ http://localhost:8080/remote
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.83s   213.53ms   2.50s    82.16%
    Req/Sec    16.58     11.91    70.00     61.48%
  Latency Distribution
     50%    1.78s 
     75%    1.89s 
     90%    2.11s 
     99%    2.39s 
  10866 requests in 1.42m, 311.50MB read
  Socket errors: connect 156, read 442, write 1, timeout 0
Requests/sec:    127.55
Transfer/sec:      3.66MB
```

----


With vectorized rand string:

DB sleep 2.

Golang baseline:
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

Clojure:

```
wrk -t12 -c400 -d240s http://localhost:8080/remote --timeout 10s --latency
Running 4m test @ http://localhost:8080/remote
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     2.08s   632.81ms   3.50s    61.29%
    Req/Sec    13.24     10.07    70.00     73.31%
  Latency Distribution
     50%    2.08s 
     75%    2.61s 
     90%    2.92s 
     99%    3.22s 
  10072 requests in 1.53m, 288.74MB read
  Socket errors: connect 156, read 672, write 2, timeout 0
Requests/sec:    109.42
Transfer/sec:      3.14MB
```


DB sleep 0.

Golang baseline:
```
wrk -t12 -c400 -d240s http://localhost:8081/db --timeout 10s --latency
Running 4m test @ http://localhost:8081/db
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.07s   553.61ms   2.95s    62.61%
    Req/Sec    23.54     15.82   111.00     74.20%
  Latency Distribution
     50%  963.74ms
     75%    1.56s 
     90%    1.81s 
     99%    2.15s 
  27954 requests in 2.18m, 1.00GB read
  Socket errors: connect 156, read 726, write 1, timeout 0
Requests/sec:    214.04
Transfer/sec:      7.87MB
```

Clojure:

```
wrk -t12 -c400 -d240s http://localhost:8080/remote --timeout 10s --latency
Running 4m test @ http://localhost:8080/remote
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.57s   249.96ms   2.06s    91.62%
    Req/Sec    16.84     12.30    70.00     70.63%
  Latency Distribution
     50%    1.63s 
     75%    1.64s 
     90%    1.67s 
     99%    1.99s 
  14395 requests in 1.66m, 412.67MB read
  Socket errors: connect 156, read 790, write 7, timeout 0
Requests/sec:    144.28
Transfer/sec:      4.14MB
```


---



Own clojure db with vectorized rand-string

sleep 2:
```
wrk -t12 -c400 -d240s http://localhost:8080/db --timeout 10s --latency
Running 4m test @ http://localhost:8080/db
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.31s   592.79ms   2.82s    59.39%
    Req/Sec    21.66     14.15    90.00     69.32%
  Latency Distribution
     50%    1.31s 
     75%    1.81s 
     90%    2.12s 
     99%    2.43s 
  19382 requests in 1.88m, 556.85MB read
  Socket errors: connect 156, read 795, write 2, timeout 0
Requests/sec:    172.27
Transfer/sec:      4.95MB
```

Sleep 0:
```
wrk -t12 -c400 -d240s http://localhost:8080/db --timeout 10s --latency
Running 4m test @ http://localhost:8080/db
  12 threads and 400 connections
^C  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.25s   367.41ms   3.24s    73.17%
    Req/Sec    21.92     14.03    90.00     73.03%
  Latency Distribution
     50%    1.31s 
     75%    1.39s 
     90%    1.56s 
     99%    2.35s 
  19650 requests in 1.78m, 565.42MB read
  Socket errors: connect 156, read 599, write 0, timeout 0
Requests/sec:    184.12
Transfer/sec:      5.30MB

```