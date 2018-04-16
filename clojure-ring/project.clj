(defproject serv "0.0.1"
  :description "Ring application for testing stress load"
  :dependencies [[org.clojure/clojure "1.9.0"]
                 [compojure "1.6.1"]
                 [ring/ring-jetty-adapter "1.6.3"]]
  :main serv.core
  :aot [serv.core]
;  :jvm-opts ["-Xmx100m" "-server"]
  :jvm-opts ["-server"])
