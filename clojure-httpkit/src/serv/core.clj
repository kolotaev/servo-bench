(ns serv.core
    (:use compojure.core
          org.httpkit.server)
    (:require [compojure.route :as route]
              [cheshire.core :as json]
              [postgres.async :as adb]
              [org.httpkit.client :as http])
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

(def db (adb/open-db {:hostname "127.0.0.1"
                  :port 5432 ; default
                  :database "postgres"
                  :username "postgres"
                  :password "root"
                  :pool-size POOL-SIZE}))

; Executors

(defn execute-db-workload [ch]
  (let [q (select-query)]
    (adb/execute! db [q]
      (fn [res err]
        (send! ch (json/encode {:users (generate-users) :query q :result res}))))))

(defn execute-remote-call [ch]
  (let [q (str "http://127.0.0.1:8081/pg/" (rand-sleep-number))]
    (http/get q
      (fn [{:keys [status headers body error]}]
        (send! ch (json/encode {:users (generate-users) :query q :result body :status status}))))))


; Endpoints
(defn root-endpoint []
  "<html>It's me, Ring App.<br/>Use routes:<br/>
  <a href='./json'>json</a><br/>
  <a href='./remote'>remote</a><br/>
  <a href='./db'>db</a></html>")

(defn json-endpoint []
  (create-user))

(defn db-endpoint [req]
  (with-channel req channel
    (execute-db-workload channel)))

(defn remote-endpoint [req]
  (with-channel req channel
    (execute-remote-call channel)))


; Main
(defroutes main-routes
  (GET "/" [] (root-endpoint))
  (GET "/json" [] (json/encode (json-endpoint)))
  (GET "/db" [] db-endpoint)
  (GET "/remote" [] remote-endpoint)
  (route/resources "/")
  (route/not-found "Sorry, page not found"))


(defn -main []
  (println (str "Running. SQL_SLEEP_MAX = " SLEEP-MAX " seconds; LOOP_COUNT = " LOOP-COUNT "; pool = " POOL-SIZE))
  (run-server main-routes {:port 8080
                          ;  :queue-size 50000
                          ;  :thread 4
                          }))
