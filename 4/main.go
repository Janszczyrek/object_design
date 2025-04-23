package main

import (
	"github.com/labstack/echo/v4"
)

func main() {
	weatherController := NewWeatherController()

	e := echo.New()
	e.GET("/weather",weatherController.getWeather)
	e.POST("/weather",weatherController.getWeather)
	e.Logger.Fatal(e.Start(":1323"))
}