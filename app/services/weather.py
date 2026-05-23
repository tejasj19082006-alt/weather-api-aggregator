import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class WeatherService:
    def __init__(self):
        # Grab the API key securely from the environment variables
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        
        # Changed base_url to the root version so we can use both /weather and /forecast endpoints
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            raise ValueError("CRITICAL: OPENWEATHER_API_KEY is missing from the environment!")

    async def get_weather_by_city(self, location_query: str):
        """
        Fetches live weather data from OpenWeatherMap.
        Accepts either "City" or "City,State".
        """
        params = {
            "q": location_query,
            "appid": self.api_key,
            "units": "metric"  # Keeps temperatures in Celsius
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/weather", params=params)
            
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

    async def get_forecast_by_city(self, location_query: str, days: int = 5):
        """
        Fetch and transform the 5-day forecast from OpenWeatherMap.
        Accepts either "City" or "City,State".
        """
        params = {
            "q": location_query,
            "appid": self.api_key,
            "units": "metric"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/forecast", params=params)
            
            if response.status_code != 200:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": response.json().get("message", "Failed to fetch forecast data")
                }
            
            raw_data = response.json()
            
            # --- TRANSFORMATION LOGIC ---
            daily_forecasts = []
            seen_dates = set()
            
            for item in raw_data.get("list", []):
                # dt_txt looks like "2024-05-25 12:00:00"
                date_str, time_str = item["dt_txt"].split(" ")
                
                # Grab the 12:00:00 PM forecast for each day
                if date_str not in seen_dates and time_str == "12:00:00":
                    daily_forecasts.append({
                        "date": date_str,
                        "temperature": item["main"]["temp"],
                        "description": item["weather"][0]["description"]
                    })
                    seen_dates.add(date_str)
                    
                # Stop parsing if we reach the requested number of days
                if len(daily_forecasts) == days:
                    break
                    
            return {
                "error": False,
                "data": daily_forecasts
            }