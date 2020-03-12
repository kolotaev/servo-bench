(ns serv.core
    (:use compojure.core)
    (:require [compojure.route :as route]
              [cheshire.core :as json]
              [clojure.java.jdbc :as jdbc]
              [ring.adapter.undertow :refer [run-undertow]])
    (:gen-class))


; Constants

(defonce SLEEP-MAX
  (Float. (or (System/getenv "SQL_SLEEP_MAX") "0")))

(defonce LOOP-COUNT
  (Integer. (or (System/getenv "LOOP_COUNT") "0")))

(defonce POOL-SIZE
  (Integer. (or (System/getenv "POOL_SIZE") "1")))


; Helpers
(defn- rand-string
  ([n]
   (let [chars  (map char (range 65 90))
         genned (take n (repeatedly #(rand-nth chars)))]
     (reduce str genned))))

(defn- create-user
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

(defn- generate-users []
  (let [users (atom ())]
    (dotimes [_ LOOP-COUNT] (swap! users conj (create-user)))
    @users))

(defn- rand-sleep-number []
  (-> SLEEP-MAX (* 1000) rand-int (/ 1000) float))

(defn- select-query []
  (let [rand-sleep (rand-sleep-number)]
    (if (== 0 rand-sleep)
      "SELECT count(*) FROM pg_catalog.pg_user"
      (str "SELECT pg_sleep(" rand-sleep ")"))))

(def db
  {:classname   "org.postgresql.Driver"
   :subprotocol "postgresql"
   :subname     (str "//127.0.0.1:5432/postgres?initial_pool_size=" POOL-SIZE "&max_idle_pool_size=" POOL-SIZE)
   :user        "postgres"
   :password    "root"})

; Executors

(defn db-endpoint []
  (let [q     (select-query)
        users (atom ())
        res   (atom "")
        rows  (jdbc/query db [q])]
    (swap! res str (first rows))
    (dotimes [_ LOOP-COUNT]
      (swap! users conj (create-user)))
    {:users @users
     :res @res
     :query q}))


; Endpoints
(defn root-endpoint []
  "<html>It's me, Undertow App.<br/>Use routes:<br/>
  <a href='./json'>json</a><br/>
  <a href='./remote'>remote</a><br/>
  <a href='./db'>db</a></html>")


; Main
(defroutes main-routes
  (GET "/" [] (root-endpoint))
  (GET "/json" [] (json/encode (create-user)))
  (GET "/db" [] (json/encode (db-endpoint)))
  (route/resources "/")
  (route/not-found "Sorry, page not found"))


(defn -main []
  (println (str "Running. SQL_SLEEP_MAX = " SLEEP-MAX " seconds; LOOP_COUNT = " LOOP-COUNT "; pool = " POOL-SIZE))
  (run-undertow main-routes {:host "0.0.0.0" :port 8080 :worker-threads POOL-SIZE}))
