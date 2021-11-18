package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"
	"io/ioutil"
	"strings"

	"github.com/labstack/echo"
	_ "github.com/lib/pq"
)

const SLEEP_MAX_DEFAULT = float64(0) // seconds
const LOOP_COUNT_DEFAULT = 0

type User struct {
	ID      string  `json:"id"`
	Name    string  `json:"name"`
	Surname string  `json:"surname"`
	Street  string  `json:"street"`
	School  string  `json:"school"`
	Bank    string  `json:"bank"`
	A       int     `json:"a"`
	B       float64 `json:"b"`
	C       int     `json:"c"`
	Friend  *User   `json:"friend"`
}

func randomString(l int) string {
	randomInt := func(min int, max int) int {
		return min + rand.Intn(max-min)
	}
	bytes := make([]byte, l)
	for i := 0; i < l; i++ {
		bytes[i] = byte(randomInt(65, 90))
	}
	return string(bytes)
}

func createUser() *User {
	friend := &User{
		ID:      randomString(34),
		Name:    randomString(10),
		Surname: randomString(3),
		Street:  randomString(15),
		School:  randomString(9),
		Bank:    randomString(4),
		A:       rand.Intn(100),
		B:       rand.Float64(),
		C:       rand.Intn(1090),
		Friend:  nil,
	}
	return &User{
		ID:      randomString(34),
		Name:    randomString(10),
		Surname: randomString(3),
		Street:  randomString(15),
		School:  randomString(9),
		Bank:    randomString(4),
		A:       rand.Intn(100),
		B:       rand.Float64(),
		C:       rand.Intn(1090),
		Friend:  friend,
	}
}

func getBenchmarkParams() (float64, int, string) {
	sleep := SLEEP_MAX_DEFAULT
	loopCount := LOOP_COUNT_DEFAULT

	f, err := strconv.ParseFloat(os.Getenv("SQL_SLEEP_MAX"), 64)
	if err == nil {
		sleep = f
	}

	i, err := strconv.Atoi(os.Getenv("LOOP_COUNT"))
	if err == nil {
		loopCount = i
	}
	return sleep, loopCount, strings.TrimSuffix(os.Getenv("TARGET_URL"), "/")
}

func randSleep(max float64) float64 {
	return rand.Float64() * max
}

func main() {
	rand.Seed(time.Now().UTC().UnixNano())

	sleep, loopCount, targetURL := getBenchmarkParams()
	log.Printf("Using SQL_SLEEP_MAX = %f seconds; LOOP_COUNT = %d\n", sleep, loopCount)

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

	e.GET("/json", func(c echo.Context) error {
		user := createUser()
		return c.JSON(http.StatusOK, &user)
	})

	e.GET("/http", func(c echo.Context) error {
		resp, err := http.Get(fmt.Sprintf("%s/%s", targetURL, randSleep(sleep)))
		if err != nil {
			c.String(http.StatusInternalServerError, err.Error())
		}
		defer resp.Body.Close()
	
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			c.String(http.StatusInternalServerError, err.Error())
		}
	
		return c.String(http.StatusOK, string(body))
	})

	e.GET("/db", func(c echo.Context) error {
		var users []*User
		result := make(map[string]interface{})

        // Do a long DB I/O call
        var queryString string
        if sleep == 0 {
            queryString = "SELECT count(*) FROM pg_catalog.pg_user"
        } else {
            queryString = fmt.Sprintf("SELECT pg_sleep(%f)", randSleep(sleep))
        }
		rows, err := db.Query(queryString)
		if err != nil {
			c.String(http.StatusInternalServerError, err.Error())
		}
		defer rows.Close()
		result["db-query"] = queryString

		// Create some CPU and RAM load
		for i := 0; i < loopCount; i++ {
			user := createUser()
			users = append(users, user)
		}
		result["data"] = users

		return c.JSON(http.StatusOK, result)
	})
	e.Start("0.0.0.0:8080")
}
