package main

import (
	"encoding/json"
	"net/http"
	"github.com/labstack/echo/v4"
)

func getWeather(c echo.Context) error {
	sampleWeather := `{
    "location": {
        "name": "Cracow",
        "region": "",
        "country": "Poland",
        "lat": 50.0833,
        "lon": 19.9167,
        "tz_id": "Europe/Warsaw",
        "localtime_epoch": 1745417300,
        "localtime": "2025-04-23 16:08"
    },
    "current": {
        "last_updated_epoch": 1745416800,
        "last_updated": "2025-04-23 16:00",
        "temp_c": 22.0,
        "temp_f": 71.6,
        "is_day": 1,
        "condition": {
            "text": "Sunny",
            "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png",
            "code": 1000
        },
        "wind_mph": 8.5,
        "wind_kph": 13.7,
        "wind_degree": 86,
        "wind_dir": "E",
        "pressure_mb": 1014.0,
        "pressure_in": 29.94,
        "precip_mm": 0.0,
        "precip_in": 0.0,
        "humidity": 41,
        "cloud": 25,
        "feelslike_c": 24.4,
        "feelslike_f": 75.9,
        "windchill_c": 19.8,
        "windchill_f": 67.7,
        "heatindex_c": 19.8,
        "heatindex_f": 67.7,
        "dewpoint_c": 8.8,
        "dewpoint_f": 47.9,
        "vis_km": 10.0,
        "vis_miles": 6.0,
        "uv": 2.4,
        "gust_mph": 10.0,
        "gust_kph": 16.1
    }
}`
var weatherData interface{}
err := json.Unmarshal([]byte(sampleWeather), &weatherData)
if err != nil {
	return c.String(http.StatusInternalServerError, "Failed to parse weather data")
}
return c.JSON(http.StatusOK, weatherData)
}