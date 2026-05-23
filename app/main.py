from fastapi import FastAPI, HTTPException
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
async def fetch_city_weather(city: str):
    """
    Retrieve current weather for a specific city and validate it against the WeatherResponse schema.
    Example: http://127.0.0.1:8000/api/v1/weather/mumbai
    """
    result = await weather_service.get_weather_by_city(city)
    
    # Handle API or Client errors safely
    if result.get("error"):
        raise HTTPException(
            status_code=result.get("status_code", 400), 
            detail=result.get("message", "An error occurred")
        )
        
    # Extract the raw OpenWeatherMap data from your service result
    raw_data = result["data"]
    
    # Map the messy raw JSON into our clean Pydantic schema format
    mapped_data = {
        "city": raw_data["name"],
        "temperature": raw_data["main"]["temp"],
        "humidity": raw_data["main"]["humidity"],
        "description": raw_data["weather"][0]["description"],
        "wind_speed": raw_data["wind"]["speed"]
    }
    
    return mapped_data

@app.get("/api/v1/forecast/{city}", response_model=ForecastResponse, tags=["Forecast"])
async def fetch_city_forecast(city: str, days: int = 5):
    """
    Retrieve a multi-day weather forecast for a specific city.
    Example: http://127.0.0.1:8000/api/v1/forecast/mumbai?days=5
    """
    # Assuming you create a get_forecast_by_city method in your WeatherService!
    # result = await weather_service.get_forecast_by_city(city, days)
    
    # if result.get("error"):
    #     raise HTTPException(status_code=result["status_code"], detail=result["message"])
    
    # raw_forecast = result["data"]
    
    # --- PLACEHOLDER RETURN ---
    # Because OpenWeatherMap's forecast data structure is complex, 
    # here is dummy data formatted to match your ForecastResponse schema 
    # so your Swagger UI works immediately while you build the actual service method.
    return {
        "city": city.capitalize(),
        "forecast_days": days,
        "forecasts": [
            {
                "date": "2024-05-25",
                "temperature": 31.0,
                "description": "clear sky"
            }
        ]
    }