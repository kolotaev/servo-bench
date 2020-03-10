
==========================
Date: Mon Mar  9 14:42:19 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | crystal-kemal |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 4170.18 |
| Req. Latency (Avg.)             | 109.86ms |
| Req. Latency (%'le - latency)   | [('50', '0.053'), ('70', '0.058'), ('90', '0.080'), ('99', '2.657'), ('99.9', '6.317'), ('99.999', '6.720')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 65 |
| Memory used samples, Mib        | [65, 65, 65, 65, 65] |
| CPU used (mean), %              | 84 |
| CPU used samples, %             | [84.2, 84.2, 84.2, 84.2, 84.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 370.83MB  |
==========================

==========================
Date: Mon Mar  9 15:24:06 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | ruby-sinatra-puma |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 1097.67 |
| Req. Latency (Avg.)             | 217.49ms |
| Req. Latency (%'le - latency)   | [('50', '0.195'), ('70', '0.217'), ('90', '0.336'), ('99', '0.683'), ('99.9', '1.039'), ('99.999', '1.913')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 78 |
| Memory used samples, Mib        | [76, 77, 78, 79, 80] |
| CPU used (mean), %              | 96 |
| CPU used samples, %             | [93.8, 99.9, 99.9, 93.8, 93.8] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 100.75MB  |
==========================

==========================
Date: Mon Mar  9 16:01:25 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | python-flask |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 894.95 |
| Req. Latency (Avg.)             | 289.49ms |
| Req. Latency (%'le - latency)   | [('50', '0.138'), ('70', '0.361'), ('90', '0.646'), ('99', '1.206'), ('99.9', '5.989'), ('99.999', '7.530')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 66 |
| Memory used samples, Mib        | [66, 66, 66, 66, 66] |
| CPU used (mean), %              | 94 |
| CPU used samples, %             | [100.0, 93.8, 87.5, 100.0, 87.6] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 93.71MB  |
==========================

==========================
Date: Mon Mar  9 16:20:45 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | clojure-httpkit |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 1905.16 |
| Req. Latency (Avg.)             | 123.60ms |
| Req. Latency (%'le - latency)   | [('50', '0.123'), ('70', '0.128'), ('90', '0.146'), ('99', '0.189'), ('99.9', '0.233'), ('99.999', '0.297')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 103 |
| Memory used samples, Mib        | [103, 103, 103, 103, 103] |
| CPU used (mean), %              | 94 |
| CPU used samples, %             | [93.3, 93.8, 93.8, 93.8, 93.8] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 189.01MB  |
==========================

==========================
Date: Mon Mar  9 17:41:28 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | js-express |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 3101.89 |
| Req. Latency (Avg.)             | 75.89ms |
| Req. Latency (%'le - latency)   | [('50', '0.076'), ('70', '0.078'), ('90', '0.083'), ('99', '0.100'), ('99.9', '0.148'), ('99.999', '0.193')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 52 |
| Memory used samples, Mib        | [52, 53, 51, 51, 51] |
| CPU used (mean), %              | 92 |
| CPU used samples, %             | [93.8, 99.9, 93.8, 87.5, 87.5] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 341.13MB  |
==========================

==========================
Date: Mon Mar  9 18:04:58 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | elixir-plug |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 2372.15 |
| Req. Latency (Avg.)             | 98.92ms |
| Req. Latency (%'le - latency)   | [('50', '0.094'), ('70', '0.098'), ('90', '0.112'), ('99', '0.201'), ('99.9', '0.258'), ('99.999', '0.593')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 189 |
| Memory used samples, Mib        | [189, 189, 189, 189, 189] |
| CPU used (mean), %              | 86 |
| CPU used samples, %             | [84.2, 78.9, 89.5, 84.2, 94.4] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 228.85MB  |
==========================

==========================
Date: Mon Mar  9 23:47:57 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | scala-play-akka |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 2128.32 |
| Req. Latency (Avg.)             | 130.77ms |
| Req. Latency (%'le - latency)   | [('50', '0.096'), ('70', '0.117'), ('90', '0.175'), ('99', '0.409'), ('99.9', '5.838'), ('99.999', '8.652')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 24  |
| Memory used (mean), Mib         | 191 |
| Memory used samples, Mib        | [192, 191, 191, 191, 191] |
| CPU used (mean), %              | 83 |
| CPU used samples, %             | [61.1, 88.9, 84.2, 90.0, 89.5] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 325.17MB  |
==========================

==========================
Date: Tue Mar 10 00:03:04 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | ruby-synchrony |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 1860.61 |
| Req. Latency (Avg.)             | 126.59ms |
| Req. Latency (%'le - latency)   | [('50', '0.118'), ('70', '0.131'), ('90', '0.147'), ('99', '0.277'), ('99.9', '0.309'), ('99.999', '0.349')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 72 |
| Memory used samples, Mib        | [72, 72, 72, 72, 72] |
| CPU used (mean), %              | 89 |
| CPU used samples, %             | [84.2, 89.5, 88.9, 94.4, 88.9] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 186.98MB  |
==========================

==========================
Date: Tue Mar 10 01:48:39 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | lua-openresty-nginx |
| Endpoint                        | /json  |
| Endpoint sleep sec. (if applicable) | 2  |
| Requests/sec                    | 4906.76 |
| Req. Latency (Avg.)             | 48.74ms |
| Req. Latency (%'le - latency)   | [('50', '0.048'), ('70', '0.049'), ('90', '0.050'), ('99', '0.058'), ('99.9', '0.249'), ('99.999', '2.081')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 50 |
| Memory used samples, Mib        | [50, 50, 50, 50, 50] |
| CPU used (mean), %              | 95 |
| CPU used samples, %             | [93.8, 99.9, 93.8, 99.9, 87.5] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/json -s wrk_report.lua --timeout 10s  |
| Data read                       | 600.79MB  |
==========================
