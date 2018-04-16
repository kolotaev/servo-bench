(ns serv.core
    (:use compojure.core
          [ring.adapter.jetty :only [run-jetty]])
    (:require [compojure.route :as route]
              [compojure.handler :as handler]
              [cheshire.core :as json])
    (:gen-class))


(defn rand-string
  ([n]
   (let [chars  (map char (range 65 90))
         genned (take n (repeatedly #(rand-nth chars)))]
     (reduce str genned))))


(defn create-user
  [friend]
  {:name (rand-string 10)
   :surname (rand-string 3)
   :street (rand-string 15)
   :school (rand-string 9)
   :bank (rand-string 4)
   :a (rand-int 100)
   :b (rand)
   :c (rand-int 1090)
   :friend friend})

(defn json-endpoint
  []
  (let [friend (create-user nil)]
    (create-user friend)))


(defn db-endpoint
  [])


(defn root-endpoint
  []
  "<html>It's me, Ring App.<br/>Use routes:<br/><a href='./json'>json</a><br/><a href='./db'>db</a></html>")


(defroutes main-routes
  (GET "/" [] (root-endpoint))
  (GET "/json" [] (json/encode (json-endpoint)))
  (GET "/db" [] (json/encode (db-endpoint)))
  (route/resources "/")
  (route/not-found "Sorry, page not found"))

(def app
  (handler/api main-routes))

(defn -main []
  (run-jetty app {:port 8080}))
