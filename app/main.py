from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from app.services.weather import WeatherService
from app.schemas import WeatherResponse, ForecastResponse

app = FastAPI(title="Weather API Aggregator")

# Initialize our weather service component
weather_service = WeatherService()

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint to verify the API is running."""
    return {"message": "Weather API Aggregator Service Layer is Active."}

@app.get("/api/v1/weather/{city}", response_model=WeatherResponse, tags=["Weather"])
async def fetch_city_weather(city: str, state: Optional[str] = Query(None, description="Optional state name")):
    """
    Retrieve current weather for a specific city (with an optional state parameter).
    Example: http://127.0.0.1:8000/api/v1/weather/mumbai?state=maharashtra
    """
    # Append state to the query if the user provided it
    search_query = f"{city},{state}" if state else city
    result = await weather_service.get_weather_by_city(search_query)
    
    if result.get("error"):
        raise HTTPException(
            status_code=result.get("status_code", 400), 
            detail=result.get("message", "An error occurred")
        )
        
    raw_data = result["data"]
    
    # Map the JSON. We also return the state if the user provided it.
    mapped_data = {
        "city": raw_data["name"],
        "state": state.title() if state else None,
        "temperature": raw_data["main"]["temp"],
        "humidity": raw_data["main"]["humidity"],
        "description": raw_data["weather"][0]["description"],
        "wind_speed": raw_data["wind"]["speed"]
    }
    
    return mapped_data

@app.get("/api/v1/forecast/{city}", response_model=ForecastResponse, tags=["Forecast"])
async def fetch_city_forecast(city: str, days: int = 5, state: Optional[str] = Query(None, description="Optional state name")):
    """
    Retrieve a multi-day weather forecast for a specific city.
    Example: http://127.0.0.1:8000/api/v1/forecast/mumbai?days=5&state=maharashtra
    """
    search_query = f"{city},{state}" if state else city
    result = await weather_service.get_forecast_by_city(search_query, days)
    
    if result.get("error"):
        raise HTTPException(
            status_code=result.get("status_code", 400), 
            detail=result.get("message", "An error occurred")
        )
    
    forecast_data = result["data"]
    
    # This structure exactly matches the ForecastResponse Pydantic Schema!
    # No more 422 errors.
    return {
        "city": city.title(),
        "state": state.title() if state else None,
        "forecast_days": len(forecast_data),
        "forecasts": forecast_data
    }