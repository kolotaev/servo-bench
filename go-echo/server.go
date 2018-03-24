package main

import (
	"net/http"
	"math/rand"
	"time"

	"github.com/labstack/echo"
)

type User struct {
  Name  string `json:"name""`
  ID string `json:"id""`
}

func randomString(l int) string {
    bytes := make([]byte, l)
    for i := 0; i < l; i++ {
        bytes[i] = byte(randInt(65, 90))
    }
    return string(bytes)
}

func randInt(min int, max int) int {
    return min + rand.Intn(max-min)
}

func main() {
	rand.Seed(time.Now().UTC().UnixNano())

	e := echo.New()
	e.GET("/json", func(c echo.Context) error {
		user := &User{
			Name: randomString(50),
			ID: randomString(10),
		}
		return c.JSON(http.StatusOK, user)
	})
	e.Start(":8080")
}
