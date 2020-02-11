(ns serv.core
    (:use compojure.core
          org.httpkit.server)
    (:require [compojure.route :as route]
              [cheshire.core :as json]
              [org.httpkit.dbcp :as db])
    (:gen-class))


(defonce SLEEP-MAX
  (Integer. (or (System/getenv "SQL_SLEEP_MAX") "0")))

(defonce LOOP-COUNT
  (Integer. (or (System/getenv "LOOP_COUNT") "0")))

(def dbconf
  {:dsn "jdbc:postgresql://127.0.0.1:5432/postgres"
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
  (let [q     (select-query)
        users (atom ())]
    (db/query q)
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


(defn -main []
  (db/use-database! (:dsn dbconf) (:user dbconf) (:password dbconf))
  (println (str "Running. SQL_SLEEP_MAX = " SLEEP-MAX " seconds; LOOP_COUNT = " LOOP-COUNT))
  (run-server main-routes {:port 8080}))
