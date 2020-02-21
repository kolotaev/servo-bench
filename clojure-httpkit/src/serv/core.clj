(ns serv.core
    (:use compojure.core
          org.httpkit.server)
    (:require [compojure.route :as route]
              [cheshire.core :as json]
              ; [postgres.async :as adb]
              [org.httpkit.client :as http]
              [hikari-cp.core :refer :all]
            [clojure.java.jdbc :as jdbc])
    (:gen-class))


; Constants

(defonce SLEEP-MAX
  (Integer. (or (System/getenv "SQL_SLEEP_MAX") "0")))

(defonce LOOP-COUNT
  (Integer. (or (System/getenv "LOOP_COUNT") "0")))


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
  (str "SELECT pg_sleep(" (rand-sleep-number) ")"))

; (def db (adb/open-db {:hostname "127.0.0.1"
;                   :port 5432 ; default
;                   :database "postgres"
;                   :username "postgres"
;                   :password "root"
;                   :pool-size 400}))

(def datasource-options {:auto-commit        true
                         :read-only          false
                         :connection-timeout 30000
                         :validation-timeout 5000
                         :idle-timeout       600000
                         :max-lifetime       1800000
                         :minimum-idle       400
                         :maximum-pool-size  400
                         :pool-name          "db-pool"
                         :adapter            "postgresql"
                         :username           "postgres"
                         :password           "root"
                         :database-name      "postgres"
                         :server-name        "localhost"
                         :port-number        5432
                         :register-mbeans    false})
; (def memoize-hikari-data-source (memoize make-hikari-data-source))
; (defn db-mysql-raw [] {:datasource (memoize-hikari-data-source)})
(defonce datasource
  (delay (make-datasource datasource-options)))
; Executors

(defn execute-db-workload []
  (let [q (select-query)]
    (jdbc/with-db-connection [conn {:datasource @datasource}]
      (let [rows (jdbc/query conn q)]
        (json/encode {:users (generate-users) :query q :result (str rows)})))))
    ; ))

    ; (adb/execute! db [q]
    ;   (fn [res err]
    ;     (send! ch (json/encode {:users (generate-users) :query q :result res}))))))

(defn execute-remote-call [ch]
  (let [q (str "http://127.0.0.1:8081/pg?sleep=" (rand-sleep-number))]
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
  (GET "/db" [] (execute-db-workload))
  (GET "/remote" [] remote-endpoint)
  (route/resources "/")
  (route/not-found "Sorry, page not found"))


(defn -main []
  (println (str "Running. SQL_SLEEP_MAX = " SLEEP-MAX " seconds; LOOP_COUNT = " LOOP-COUNT))
  (run-server main-routes {:port 8080
                          ;  :queue-size 50000
                           :thread 400
                          }))
