(ns serv.core
    (:use compojure.core
          [ring.adapter.jetty :only [run-jetty]])
    (:require [compojure.route :as route]
              [compojure.handler :as handler])
    (:gen-class))




(defroutes main-routes
  (GET "/" [] "Powered by foo")
  (GET "/json" (json-endpoint))
  (GET "/db" (db-endpoint))

  (route/resources "/")
  (route/not-found "Page not found"))

(def app
  (handler/api main-routes))

(defn -main []
  (run-jetty app {:port 8080}))
