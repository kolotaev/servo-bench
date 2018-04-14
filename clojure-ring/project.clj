(defproject helloworld "0.1.0-SNAPSHOT"
  :description "very basic ring application"
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [ring/ring-core "1.5.0"]
                 [ring/ring-jetty-adapter "1.5.0"]]
  :main jetty-my.core
  :aot [jetty-my.core]
  :jvm-opts ["-Xmx100m" "-server"])
