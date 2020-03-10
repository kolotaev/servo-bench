==========================
Date: Mon Mar  9 14:50:18 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | crystal-kemal |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 213.00 |
| Req. Latency (Avg.)             | 1.11s |
| Req. Latency (%'le - latency)   | [('50', '1.102'), ('70', '1.509'), ('90', '1.916'), ('99', '2.612'), ('99.9', '4.302'), ('99.999', '5.223')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 119 |
| Memory used samples, Mib        | [116, 115, 115, 114, 133] |
| CPU used (mean), %              | 76 |
| CPU used samples, %             | [73.7, 75.0, 77.8, 78.9, 75.0] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.34GB  |
==========================

==========================
Date: Mon Mar  9 15:30:12 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | ruby-sinatra-puma |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 69.58 |
| Req. Latency (Avg.)             | 3.34s |
| Req. Latency (%'le - latency)   | [('50', '3.357'), ('70', '3.913'), ('90', '4.647'), ('99', '6.153'), ('99.9', '7.340'), ('99.999', '9.081')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 1  |
| Memory used (mean), Mib         | 160 |
| Memory used samples, Mib        | [160, 160, 160, 161, 161] |
| CPU used (mean), %              | 92 |
| CPU used samples, %             | [94.1, 94.4, 87.5, 88.2, 94.1] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 476.05MB  |
==========================

==========================
Date: Mon Mar  9 16:07:31 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | python-flask |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 69.62 |
| Req. Latency (Avg.)             | 3.12s |
| Req. Latency (%'le - latency)   | [('50', '0.050'), ('70', '6.182'), ('90', '7.224'), ('99', '9.297'), ('99.9', '9.805'), ('99.999', '9.935')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 209  |
| Memory used (mean), Mib         | 123 |
| Memory used samples, Mib        | [119, 121, 123, 125, 127] |
| CPU used (mean), %              | 84 |
| CPU used samples, %             | [80.0, 94.8, 83.3, 89.5, 70.0] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 480.75MB  |
==========================

==========================
Date: Mon Mar  9 16:54:32 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | clojure-httpkit |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 56.20 |
| Req. Latency (Avg.)             | 4.17s |
| Req. Latency (%'le - latency)   | [('50', '4.112'), ('70', '4.638'), ('90', '5.452'), ('99', '6.752'), ('99.9', '8.095'), ('99.999', '8.908')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 119 |
| Memory used samples, Mib        | [118, 120, 118, 120, 121] |
| CPU used (mean), %              | 89 |
| CPU used samples, %             | [88.9, 88.9, 88.9, 88.9, 88.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 387.68MB  |
==========================

==========================
Date: Mon Mar  9 17:51:03 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | js-express |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 232.00 |
| Req. Latency (Avg.)             | 1.01s |
| Req. Latency (%'le - latency)   | [('50', '1.015'), ('70', '1.419'), ('90', '1.812'), ('99', '1.989'), ('99.9', '2.013'), ('99.999', '2.530')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 62 |
| Memory used samples, Mib        | [61, 62, 62, 62, 62] |
| CPU used (mean), %              | 38 |
| CPU used samples, %             | [52.9, 37.5, 31.2, 29.4, 41.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.40GB  |
==========================

==========================
Date: Mon Mar  9 19:04:33 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | elixir-plug |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 147.83 |
| Req. Latency (Avg.)             | 1.60s |
| Req. Latency (%'le - latency)   | [('50', '1.597'), ('70', '2.002'), ('90', '2.464'), ('99', '3.594'), ('99.9', '3.994'), ('99.999', '4.304')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 243 |
| Memory used samples, Mib        | [249, 255, 227, 241, 243] |
| CPU used (mean), %              | 75 |
| CPU used samples, %             | [68.0, 73.9, 78.3, 72.7, 81.0] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 0.93GB  |
==========================

==========================
Date: Mon Mar  9 23:55:01 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | scala-play-akka |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 208.61 |
| Req. Latency (Avg.)             | 1.13s |
| Req. Latency (%'le - latency)   | [('50', '1.124'), ('70', '1.535'), ('90', '1.932'), ('99', '2.565'), ('99.9', '3.020'), ('99.999', '4.713')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 271 |
| Memory used samples, Mib        | [262, 261, 278, 281, 273] |
| CPU used (mean), %              | 73 |
| CPU used samples, %             | [78.9, 78.9, 84.2, 42.1, 78.9] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.43GB  |
==========================

==========================
Date: Tue Mar 10 00:13:19 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | ruby-synchrony |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 97.48 |
| Req. Latency (Avg.)             | 2.40s |
| Req. Latency (%'le - latency)   | [('50', '2.415'), ('70', '2.806'), ('90', '3.219'), ('99', '3.483'), ('99.9', '3.652'), ('99.999', '3.872')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 88 |
| Memory used samples, Mib        | [88, 88, 88, 88, 89] |
| CPU used (mean), %              | 47 |
| CPU used samples, %             | [61.1, 57.9, 25.0, 55.6, 36.8] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 667.81MB  |
==========================

==========================
Date: Tue Mar 10 11:45:22 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | lua-openresty-nginx |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 177.23 |
| Req. Latency (Avg.)             | 1.33s |
| Req. Latency (%'le - latency)   | [('50', '1.315'), ('70', '1.734'), ('90', '2.145'), ('99', '2.844'), ('99.9', '3.719'), ('99.999', '4.140')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 56 |
| Memory used samples, Mib        | [56, 56, 56, 56, 56] |
| CPU used (mean), %              | 82 |
| CPU used samples, %             | [88.2, 77.8, 82.4, 83.3, 77.8] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.49GB  |
==========================
