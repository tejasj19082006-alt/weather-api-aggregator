from fastapi import FastAPI, HTTPException
from app.services.weather import WeatherService

app = FastAPI(title="Weather API Aggregator")

# Initialize our weather service component
weather_service = WeatherService()

@app.get("/")
def home():
    return {"message": "Weather API Aggregator Service Layer is Active."}

@app.get("/weather/{city}")
async def fetch_city_weather(city: str):
    """
    Endpoint to retrieve current weather for a specific city.
    Example: http://127.0.0.1:8000/weather/mumbai
    """
    result = await weather_service.get_weather_by_city(city)
    
    # Handle API or Client errors safely
    if result["error"]:
        raise HTTPException(
            status_code=result["status_code"], 
            detail=result["message"]
        )
        
    return result["data"]