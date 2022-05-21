package main

import (
	"fmt"
	"net/http"
	"time"
	"strings"
	"strconv"
	"math/rand"
	"os"
)

func main() {
	max_sleep := 0.0
	f, err := strconv.ParseFloat(os.Getenv("SQL_SLEEP_MAX"), 64)
	if err == nil {
		max_sleep = f
	}

	mux := http.NewServeMux()

	mux.HandleFunc("/sleep/", func(w http.ResponseWriter, req *http.Request) {
		parts := strings.Split(strings.Trim(req.URL.Path, "/"), "/")
		if len(parts) != 2 {
			er(w, "Please, specify number of seconds to sleep before echoing back")
			return
		}
		sleep, err := strconv.ParseFloat(parts[1], 64)
		if err != nil {
			er(w, "Sleep time should be a Number")
			return
		}

		time.Sleep(time.Duration(sleep) * time.Second)
		success(w, sleep)
	})

	mux.HandleFunc("/sleep-me/", func(w http.ResponseWriter, req *http.Request) {
		sleep := randSleep(max_sleep)
		time.Sleep(time.Duration(sleep) * time.Second)
		success(w, sleep)
	})

	http.ListenAndServe("0.0.0.0:9000", mux)
}

func randSleep(max float64) float64 {
	return rand.Float64() * max
}

func er(w http.ResponseWriter, message string) {
	w.WriteHeader(http.StatusInternalServerError)
	fmt.Fprint(w, fmt.Sprintf(`{"error": "%s"}`, message))
}

func success(w http.ResponseWriter, sleep float64) {
	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, fmt.Sprintf(`{"slept": "%f"}`, sleep))
}
