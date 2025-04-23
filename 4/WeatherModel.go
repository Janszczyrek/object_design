package main

import (
    "gorm.io/gorm"
)

type WeatherData struct {
    Location Location `json:"location"`
    Current  Current  `json:"current"`
}

type Location struct {
    gorm.Model
    Name           string  `json:"name"`
    Region         string  `json:"region"`
    Country        string  `json:"country"`
    Lat            float64 `json:"lat"`
    Lon            float64 `json:"lon"`
    TzID           string  `json:"tz_id"`
    LocaltimeEpoch int64   `json:"localtime_epoch"`
    Localtime      string  `json:"localtime"`
}

type Current struct {
    gorm.Model
    LastUpdatedEpoch int64     `json:"last_updated_epoch"`
    TempC            float64   `json:"temp_c"`
    WindKph          float64   `json:"wind_kph"`
    PressureMb       float64   `json:"pressure_mb"`
    PrecipMm         float64   `json:"precip_mm"`
    Humidity         int       `json:"humidity"`
    FeelslikeC       float64   `json:"feelslike_c"`
    HeatindexC       float64   `json:"heatindex_c"`
    DewpointC        float64   `json:"dewpoint_c"`
    VisKm            float64   `json:"vis_km"`
    UV               float64   `json:"uv"`
    GustKph          float64   `json:"gust_kph"`
}
