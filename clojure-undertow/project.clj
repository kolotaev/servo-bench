(defproject serv "0.0.1"
  :description "Clojure Ring on Undertow application for testing stress load"
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [compojure "1.6.1"]
                 [cheshire "5.8.0"]
                 [org.clojure/java.jdbc "0.7.11"]
                 [org.postgresql/postgresql "42.2.2.jre7"]
                 [ring-undertow-adapter "0.2.2"]]
  :main serv.core
  :uberjar {:aot :all}
  :uberjar-name "serv-standalone.jar"
  :jvm-opts ["-server"])
