package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/labstack/echo"
	_ "github.com/lib/pq"
)

func main() {
	// Connect to DB
	connStr := "postgres://postgres:root@127.0.0.1/postgres?sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	if err = db.Ping(); err != nil {
		panic(err)
	} else {
		log.Println("DB Connected...")
	}

	e := echo.New()

	e.GET("/ping", func(c echo.Context) error {
		return c.JSON(http.StatusOK, "pong")
	})

	e.GET("/sleep/:ms", func(c echo.Context) error {
		milliseconds, err := strconv.Atoi(c.Param("ms"))
		if err != nil {
			log.Fatal(err)
		}
		time.Sleep(time.Duration(milliseconds) * time.Millisecond)
		return c.JSON(http.StatusOK, fmt.Sprintf("i was sleeping %d milliseconds", milliseconds))
	})

	e.GET("/pg/:seconds", func(c echo.Context) error {
		seconds, err := strconv.ParseFloat(c.Param("seconds"), 64)
		if err != nil {
			log.Fatal(err)
		}
		var result string
		var result2 float64
		row := db.QueryRow(fmt.Sprintf("SELECT pg_sleep(%f), %f", seconds, seconds))
		err = row.Scan(&result, &result2)
		if err != nil {
			log.Fatal(err)
		}
		return c.JSON(http.StatusOK, result2)
	})

	e.Start("0.0.0.0:8081")
}
