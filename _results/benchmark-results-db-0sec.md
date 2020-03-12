
==========================
Date: Wed Mar 11 14:17:38 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | ruby-sinatra-puma |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 70.21 |
| Req. Latency (Avg.)             | 3.34s |
| Req. Latency (%'le - latency)   | [('50', '3.228'), ('70', '3.410'), ('90', '4.394'), ('99', '5.999'), ('99.9', '7.900'), ('99.999', '9.326')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 3  |
| Memory used (mean), Mib         | 160 |
| Memory used samples, Mib        | [160, 160, 160, 161, 161] |
| CPU used (mean), %              | 87 |
| CPU used samples, %             | [73.7, 88.9, 88.2, 88.9, 93.8] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 480.46MB  |
==========================

==========================
Date: Wed Mar 11 14:24:47 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | crystal-kemal |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 273.55 |
| Req. Latency (Avg.)             | 856.15ms |
| Req. Latency (%'le - latency)   | [('50', '0.793'), ('70', '0.839'), ('90', '1.065'), ('99', '1.697'), ('99.9', '2.298'), ('99.999', '3.667')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 65 |
| Memory used samples, Mib        | [65, 65, 65, 65, 65] |
| CPU used (mean), %              | 75 |
| CPU used samples, %             | [70.0, 77.8, 73.7, 70.0, 83.3] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.72GB  |
==========================

==========================
Date: Thu Mar 12 11:09:50 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | python-flask |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 61.97 |
| Req. Latency (Avg.)             | 3.31s |
| Req. Latency (%'le - latency)   | [('50', '3.904'), ('70', '5.310'), ('90', '8.237'), ('99', '9.754'), ('99.9', '9.910'), ('99.999', '9.996')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 652  |
| Memory used (mean), Mib         | 118 |
| Memory used samples, Mib        | [117, 117, 118, 119, 121] |
| CPU used (mean), %              | 87 |
| CPU used samples, %             | [84.2, 94.8, 89.5, 84.2, 84.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 428.09MB  |
==========================

==========================
Date: Thu Mar 12 11:23:05 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | clojure-httpkit |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 53.20 |
| Req. Latency (Avg.)             | 4.41s |
| Req. Latency (%'le - latency)   | [('50', '4.200'), ('70', '4.385'), ('90', '5.600'), ('99', '7.035'), ('99.9', '8.509'), ('99.999', '8.711')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 119 |
| Memory used samples, Mib        | [119, 120, 119, 118, 118] |
| CPU used (mean), %              | 82 |
| CPU used samples, %             | [88.9, 88.9, 84.2, 66.7, 83.3] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 367.52MB  |
==========================

==========================
Date: Thu Mar 12 14:20:10 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | js-express |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 496.52 |
| Req. Latency (Avg.)             | 477.62ms |
| Req. Latency (%'le - latency)   | [('50', '0.469'), ('70', '0.530'), ('90', '0.628'), ('99', '1.067'), ('99.9', '1.686'), ('99.999', '2.260')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 62 |
| Memory used samples, Mib        | [62, 62, 62, 63, 63] |
| CPU used (mean), %              | 82 |
| CPU used samples, %             | [74.1, 88.2, 76.5, 82.4, 88.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 3.13GB  |
==========================

==========================
Date: Thu Mar 12 15:35:28 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | elixir-plug |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 221.07 |
| Req. Latency (Avg.)             | 1.07s |
| Req. Latency (%'le - latency)   | [('50', '1.033'), ('70', '1.073'), ('90', '1.192'), ('99', '1.966'), ('99.9', '2.135'), ('99.999', '2.379')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 232 |
| Memory used samples, Mib        | [231, 231, 232, 232, 232] |
| CPU used (mean), %              | 78 |
| CPU used samples, %             | [78.9, 83.3, 73.7, 82.4, 73.7] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.40GB  |
==========================

==========================
Date: Thu Mar 12 15:43:11 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | scala-play-akka |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 218.18 |
| Req. Latency (Avg.)             | 1.08s |
| Req. Latency (%'le - latency)   | [('50', '1.011'), ('70', '1.201'), ('90', '1.607'), ('99', '2.576'), ('99.9', '3.142'), ('99.999', '3.366')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 247 |
| Memory used samples, Mib        | [246, 245, 247, 248, 247] |
| CPU used (mean), %              | 86 |
| CPU used samples, %             | [88.9, 84.2, 84.2, 89.5, 84.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.49GB  |
==========================

==========================
Date: Thu Mar 12 16:39:49 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | ruby-synchrony |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 183.34 |
| Req. Latency (Avg.)             | 1.29s |
| Req. Latency (%'le - latency)   | [('50', '1.230'), ('70', '1.266'), ('90', '1.386'), ('99', '2.470'), ('99.9', '2.650'), ('99.999', '3.408')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 91 |
| Memory used samples, Mib        | [91, 91, 91, 91, 91] |
| CPU used (mean), %              | 81 |
| CPU used samples, %             | [75.0, 71.4, 88.9, 85.0, 84.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.23GB  |
==========================

==========================
Date: Thu Mar 12 17:32:47 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | python-aiohttp |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 74.08 |
| Req. Latency (Avg.)             | 3.17s |
| Req. Latency (%'le - latency)   | [('50', '3.115'), ('70', '3.206'), ('90', '3.510'), ('99', '5.596'), ('99.9', '5.961'), ('99.999', '6.753')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 53 |
| Memory used samples, Mib        | [53, 53, 53, 53, 52] |
| CPU used (mean), %              | 81 |
| CPU used samples, %             | [72.0, 82.4, 88.2, 77.8, 82.4] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 571.16MB  |
==========================

==========================
Date: Thu Mar 12 17:55:48 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | clojure-undertow |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 32.75 |
| Req. Latency (Avg.)             | 5.82s |
| Req. Latency (%'le - latency)   | [('50', '5.981'), ('70', '7.347'), ('90', '8.965'), ('99', '9.867'), ('99.9', '9.987'), ('99.999', '9.997')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 1360  |
| Memory used (mean), Mib         | 216 |
| Memory used samples, Mib        | [207, 219, 221, 219, 212] |
| CPU used (mean), %              | 82 |
| CPU used samples, %             | [75.0, 93.8, 93.8, 66.7, 82.4] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 226.33MB  |
==========================

==========================
Date: Thu Mar 12 18:25:38 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | go-echo |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 206.37 |
| Req. Latency (Avg.)             | 1.15s |
| Req. Latency (%'le - latency)   | [('50', '1.060'), ('70', '1.551'), ('90', '1.923'), ('99', '2.445'), ('99.9', '2.978'), ('99.999', '3.502')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 0  |
| Memory used (mean), Mib         | 33 |
| Memory used samples, Mib        | [32, 32, 33, 33, 33] |
| CPU used (mean), %              | 47 |
| CPU used samples, %             | [44.4, 50.0, 44.4, 44.4, 52.9] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.78GB  |
==========================

==========================
Date: Thu Mar 12 18:44:05 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | clojure-ring-jetty |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 35.52 |
| Req. Latency (Avg.)             | 3.44s |
| Req. Latency (%'le - latency)   | [('50', '1.668'), ('70', '6.335'), ('90', '8.776'), ('99', '9.874'), ('99.9', '9.986'), ('99.999', '9.998')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 2404  |
| Memory used (mean), Mib         | 210 |
| Memory used samples, Mib        | [193, 208, 218, 223, 209] |
| CPU used (mean), %              | 70 |
| CPU used samples, %             | [66.7, 84.2, 85.0, 35.0, 78.9] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 245.29MB  |
==========================

==========================
Date: Thu Mar 12 19:28:00 2020
Results:

| Param                           | Value |
| :---                            | :--- |
| Framework                       | lua-openresty-nginx |
| Endpoint                        | /db  |
| Endpoint sleep sec. (if applicable) | 0.0  |
| Requests/sec                    | 172.70 |
| Req. Latency (Avg.)             | 1.27s |
| Req. Latency (%'le - latency)   | [('50', '1.074'), ('70', '1.224'), ('90', '2.467'), ('99', '3.330'), ('99.9', '5.464'), ('99.999', '9.908')] |
| 5xx/4xx responses               | 0 |
| N timeout-ed                    | 136  |
| Memory used (mean), Mib         | 54 |
| Memory used samples, Mib        | [54, 54, 54, 54, 54] |
| CPU used (mean), %              | 76 |
| CPU used samples, %             | [81.2, 93.8, 61.1, 72.2, 72.2] |
| Test command                    | wrk -t12 -c400 -d240s http://localhost:8080/db -s wrk_report.lua --timeout 10s  |
| Data read                       | 1.45GB  |
==========================
