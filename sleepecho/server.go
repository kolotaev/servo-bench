package main

import (
	"fmt"
	"net/http"
	"time"
	"strings"
	"strconv"
)

func main() {

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
		
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, fmt.Sprintf(`{"slept": "%f"}`, sleep))
	})

	http.ListenAndServe("0.0.0.0:9000", mux)
}

func er(w http.ResponseWriter, message string) {
	w.WriteHeader(http.StatusInternalServerError)
	fmt.Fprint(w, fmt.Sprintf(`{"error": "%s"}`, message))
}
