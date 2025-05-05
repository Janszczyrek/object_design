package main
import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
	"os"
)

type WeatherProxy struct {
	cachedWeather WeatherData
	cachedTime  int64
}

func NewWeatherProxy() *WeatherProxy {
	return &WeatherProxy{}
}
func (wp *WeatherProxy) GetWeather() WeatherData {
	if (wp.cachedWeather == WeatherData{}) {
		err := wp.fetchWeather()
		if err != nil {
			log.Println("Error fetching weather data:", err)
		}
	}
	if (time.Now().Unix()-wp.cachedTime > 600) {
		err := wp.fetchWeather()
		if err != nil {
			log.Println("Error fetching weather data:", err)
		}
	}
	return wp.cachedWeather
}
func (wp *WeatherProxy) fetchWeather() error {
	apiKey := os.Getenv("WEATHER_API_KEY")
	if apiKey == "" {
		log.Fatal("API key not set")
	}
	resp, err := http.Get("https://api.weatherapi.com/v1/current.json?key=" + apiKey + "&q=Cracow")
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		log.Fatalf("Error: %s", resp.Status)
	}
	
	var newData WeatherData
	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
        return fmt.Errorf("failed to read response body: %w", err)
    }
	err = json.Unmarshal(bodyBytes, &newData)
	wp.cachedWeather = newData
	wp.cachedTime = time.Now().Unix()
	log.Println("Weather data fetched successfully")
	return nil
}