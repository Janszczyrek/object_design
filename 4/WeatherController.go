package main

import (
	"net/http"
	"github.com/labstack/echo/v4"
)
type WeatherController struct {
	weatherData WeatherData
	weatherProxy *WeatherProxy
}

func NewWeatherController() *WeatherController {
	weatherProxy := NewWeatherProxy()
	weatherData := weatherProxy.GetWeather()
	return &WeatherController{
		weatherData: weatherData,
		weatherProxy: weatherProxy,
	}
}

func (wc *WeatherController) getWeather(c echo.Context) error {
	wc.weatherData = wc.weatherProxy.GetWeather()
	return c.JSON(http.StatusOK, wc.weatherData)
}