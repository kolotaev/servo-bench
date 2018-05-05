(ns serv.core
    (:use compojure.core
          [ring.adapter.jetty :only [run-jetty]])
    (:require [compojure.route :as route]
              [clojure.java.jdbc :as sql]
              [compojure.handler :as handler]
              [cheshire.core :as json])
    (:gen-class))


(def SLEEP-MAX
  (Integer. (or (System/getenv "SQL_SLEEP_MAX") "0")))

(def LOOP-COUNT
  (Integer. (or (System/getenv "LOOP_COUNT") "0")))

(def db
  {:classname   "org.postgresql.Driver"
   :subprotocol "postgresql"
   :subname     "//127.0.0.1:5432/postgres"
   :user        "postgres"
   :password    "root"})


; Helpers
(defn rand-string
  ([n]
   (let [chars  (map char (range 65 90))
         genned (take n (repeatedly #(rand-nth chars)))]
     (reduce str genned))))

(defn create-user
  [& [no-friends?]]
  {:name    (rand-string 10)
   :surname (rand-string 3)
   :street  (rand-string 15)
   :school  (rand-string 9)
   :bank    (rand-string 4)
   :a       (rand-int 100)
   :b       (rand)
   :c       (rand-int 1090)
   :friend  (when-not no-friends?
                      (create-user true))})

(defn select-query []
  (str "SELECT pg_sleep(" (-> SLEEP-MAX (* 1000) rand-int (/ 1000) float) ")"))


; Endpoints
(defn json-endpoint []
  (create-user))

(defn db-endpoint []
  (let [q      (select-query)
        users (atom ())]
    (sql/query db [q])
    (dotimes [_ LOOP-COUNT]
      (swap! users conj (create-user)))
    {:users @users
     :query q}))


(defn root-endpoint []
  "<html>It's me, Ring App.<br/>Use routes:<br/><a href='./json'>json</a><br/><a href='./db'>db</a></html>")


; Main
(defroutes main-routes
  (GET "/" [] (root-endpoint))
  (GET "/json" [] (json/encode (json-endpoint)))
  (GET "/db" [] (json/encode (db-endpoint)))
  (route/resources "/")
  (route/not-found "Sorry, page not found"))

(def app
  (handler/api main-routes))

(defn -main []
  (println (str "Running. SQL_SLEEP_MAX = " SLEEP-MAX " seconds; LOOP_COUNT = " LOOP-COUNT))
  (run-jetty app {:port 8080}))
