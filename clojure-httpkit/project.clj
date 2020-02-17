(defproject serv "0.0.1"
  :description "Clojure Http-kit application for testing stress load"
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [compojure "1.6.1"]
                 [cheshire "5.8.0"]
                 [http-kit "2.3.0"]
                ;  [http-kit/dbcp "0.1.0"]
                ;  [postgresql/postgresql "8.4-702.jdbc4"]
                ;  [clj-http "3.10.0"]
                ;  [alaisi/postgres.async "0.8.0"]
                 ]
  :main serv.core
;  :aot [serv.core]
  :uberjar {:aot :all}
  :uberjar-name "serv-standalone.jar"
;  :jvm-opts ["-Xmx100m" "-server"]
  :jvm-opts ["-server"])
