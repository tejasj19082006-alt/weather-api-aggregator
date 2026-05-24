from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from app.services.weather import WeatherService
from app.schemas import WeatherResponse, ForecastResponse

app = FastAPI(title="Weather API Aggregator")
weather_service = WeatherService()

@app.get("/api/v1/weather/{city}", response_model=WeatherResponse)
async def fetch_city_weather(city: str, state: Optional[str] = Query(None)):
    # 1. Clean the inputs to remove accidental spaces!
    clean_city = city.strip()
    clean_state = state.strip() if state else None

    # 2. Build the query using the clean variables
    search_query = f"{clean_city},{clean_state}" if clean_state else clean_city
    result = await weather_service.get_weather_by_city(search_query)
    
    if result.get("error"):
        raise HTTPException(status_code=result.get("status_code", 500), detail=result.get("message"))
        
    data = result["data"]
    return {
        "city": data.get("name", clean_city),
        "state": clean_state.title() if clean_state else None,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

@app.get("/api/v1/forecast/{city}", response_model=ForecastResponse)
async def fetch_city_forecast(city: str, days: int = 5, state: Optional[str] = Query(None)):
    # 1. Clean the inputs
    clean_city = city.strip()
    clean_state = state.strip() if state else None

    # 2. Build the query using the clean variables
    search_query = f"{clean_city},{clean_state}" if clean_state else clean_city
    result = await weather_service.get_forecast_by_city(search_query, days)
    
    if result.get("error"):
        raise HTTPException(status_code=result.get("status_code", 500), detail=result.get("message"))
    
    return {
        "city": clean_city.title(),
        "state": clean_state.title() if clean_state else None,
        "forecast_days": len(result["data"]),
        "forecasts": result["data"]
    }