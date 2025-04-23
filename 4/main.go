package main

import (
	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	e.GET("/weather",getWeather)
	e.POST("/weather",getWeather)
	e.Logger.Fatal(e.Start(":1323"))
}