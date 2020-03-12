(ns serv.core
    (:use compojure.core
          [ring.adapter.jetty :only [run-jetty]])
    (:require [compojure.route :as route]
              [clojure.java.jdbc :as jdbc]
              [hikari-cp.core :refer :all]
              [compojure.handler :as handler]
              [cheshire.core :as json])
    (:gen-class))


(defonce SLEEP-MAX
  (Float. (or (System/getenv "SQL_SLEEP_MAX") "0")))

(defonce LOOP-COUNT
  (Integer. (or (System/getenv "LOOP_COUNT") "0")))

(defonce POOL-SIZE
  (Integer. (or (System/getenv "POOL_SIZE") "1")))

(def datasource-options {:auto-commit        true
                         :read-only          false
                         :connection-timeout 30000
                         :validation-timeout 5000
                         :idle-timeout       600000
                         :max-lifetime       1800000
                         :minimum-idle       POOL-SIZE
                         :maximum-pool-size  POOL-SIZE
                         :pool-name          "db-pool"
                         :adapter            "postgresql"
                         :username           "postgres"
                         :password           "root"
                         :database-name      "postgres"
                         :server-name        "localhost"
                         :port-number        5432
                         :register-mbeans    false})

(defonce datasource
  (delay (make-datasource datasource-options)))

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

(defn- rand-sleep-number []
  (-> SLEEP-MAX (* 1000) rand-int (/ 1000) float))

(defn- select-query []
  (let [rand-sleep (rand-sleep-number)]
    (if (== 0 rand-sleep)
      "SELECT count(*) FROM pg_catalog.pg_user"
      (str "SELECT pg_sleep(" rand-sleep ")"))))


; Endpoints
(defn json-endpoint []
  (create-user))

(defn db-endpoint []
  (let [q     (select-query)
        users (atom ())
        res   (atom "")]
    (jdbc/with-db-connection [conn {:datasource @datasource}]
      (let [rows (jdbc/query conn q)]
        (swap! res str (first rows))))
    (dotimes [_ LOOP-COUNT]
      (swap! users conj (create-user)))
    {:users @users
     :res @res
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
  (println (str "Running. SQL_SLEEP_MAX = " SLEEP-MAX " seconds; LOOP_COUNT = " LOOP-COUNT "; pool = " POOL-SIZE))
  (run-jetty app {:port 8080
                  :min-threads 200
                  :max-threads 400}))
