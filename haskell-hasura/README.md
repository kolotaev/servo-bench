### Hasura tests.

> Not participating in the competition yet.

### How to run:

```
wrk -t12 -c400 -d240s http://localhost:8080/v1/graphql --timeout 10s --latency --script hasura/graphql.lua
```


### Results:

_Note that we don't use loop 100 to smulate post work here_

For users count:

```
wrk -t12 -c400 -d240s http://localhost:8080/v1/graphql --timeout 10s --latency --script hasura/graphql.lua
Running 4m test @ http://localhost:8080/v1/graphql
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   193.82ms   23.43ms 681.16ms   92.65%
    Req/Sec   112.52     68.45   383.00     61.43%
  Latency Distribution
     50%  195.71ms
     75%  203.75ms
     90%  208.93ms
     99%  231.36ms
  291253 requests in 4.00m, 70.55MB read
  Socket errors: connect 156, read 710, write 0, timeout 0
Requests/sec:   1213.07
Transfer/sec:    300.90KB
```

but with PG pool size 400 it gives:

```
wrk -t12 -c400 -d240s http://localhost:8080/v1/graphql --timeout 10s --latency --script hasura/graphql.lua
Running 4m test @ http://localhost:8080/v1/graphql
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   197.88ms   55.81ms   2.25s    92.78%
    Req/Sec   109.28     60.34   420.00     62.12%
  Latency Distribution
     50%  191.86ms
     75%  202.18ms
     90%  214.24ms
     99%  368.68ms
  285956 requests in 4.00m, 69.27MB read
  Socket errors: connect 156, read 697, write 0, timeout 0
Requests/sec:   1191.02
Transfer/sec:    295.43KB
```

Memory taken: 142.7 MiB	graphql-engine

CPU taken: ~ 70 - 80 %



For random sleep 2 sec:

```
wrk -t12 -c400 -d240s http://localhost:8080/v1/graphql --timeout 10s --latency --script hasura/graphql.lua
Running 4m test @ http://localhost:8080/v1/graphql
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.00s   576.13ms   2.34s    57.87%
    Req/Sec    26.54     16.80   110.00     61.55%
  Latency Distribution
     50%    1.00s 
     75%    1.50s 
     90%    1.80s 
     99%    1.98s 
  56222 requests in 4.00m, 13.83MB read
  Socket errors: connect 156, read 732, write 0, timeout 0
Requests/sec:    234.17
Transfer/sec:     59.00KB
```

Memory taken: 160.7 MiB	graphql-engine
              386.5 MiB	postgres (248)

CPU taken: ~ 15 - 25 %
