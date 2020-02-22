(defproject serv "0.0.1"
  :description "Ring application for testing stress load"
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [compojure "1.6.1"]
                 [ring/ring-jetty-adapter "1.6.3"]
                 [cheshire "5.8.0"]
                 [org.clojure/java.jdbc "0.7.11"]
                 [org.postgresql/postgresql "42.2.2.jre7"]
                 [hikari-cp "2.10.0"]]
  :main serv.core
  :uberjar {:aot :all}
  :uberjar-name "serv-standalone.jar"
;  :jvm-opts ["-Xmx100m" "-server"]
  :jvm-opts ["-server"])
