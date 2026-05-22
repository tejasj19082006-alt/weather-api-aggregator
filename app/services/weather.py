import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        # Grab the API key securely from the environment variables
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            raise ValueError("CRITICAL: OPENWEATHER_API_KEY is missing from the environment!")

    async def get_weather_by_city(self, city: str):
        """
        Fetches live weather data from OpenWeatherMap for a given city.
        Uses AsyncClient for high-performance non-blocking I/O.
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Keeps temperatures in Celsius
        }
        
        # Use httpx.AsyncClient for asynchronous requests matching FastAPI's design
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            
            # If the HTTP request failed (e.g., 404 city not found, 401 unauthorized key)
            if response.status_code != 200:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": response.json().get("message", "Failed to fetch weather data")
                }
                
            return {
                "error": False,
                "data": response.json()
            }