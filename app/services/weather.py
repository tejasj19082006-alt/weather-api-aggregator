import os
import httpx
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache = TTLCache(maxsize=100, ttl=600)

    async def _fetch_from_api(self, endpoint: str, params: dict):
        """Helper to handle HTTP requests safely with robust error handling."""
        params["appid"] = self.api_key
        params["units"] = "metric"
        
        # We add a timeout so our server doesn't hang forever if OpenWeatherMap is slow
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/{endpoint}", params=params)
                
                # Check for specific HTTP error codes from OpenWeatherMap
                if response.status_code == 401:
                    return {"error": True, "status_code": 401, "message": "Invalid API Key"}
                elif response.status_code == 404:
                    return {"error": True, "status_code": 404, "message": "Location not found"}
                elif response.status_code == 429:
                    return {"error": True, "status_code": 429, "message": "API rate limit exceeded"}
                
                # Raise an exception for any other 4xx or 5xx errors
                response.raise_for_status()
                
                return {"error": False, "data": response.json()}
                
            except httpx.ConnectTimeout:
                return {"error": True, "status_code": 504, "message": "Connection to Weather Provider timed out"}
            except httpx.ConnectError:
                return {"error": True, "status_code": 503, "message": "Failed to connect to Weather Provider"}
            except httpx.HTTPStatusError as e:
                # Catch-all for other HTTP errors not explicitly handled above
                return {"error": True, "status_code": response.status_code, "message": f"External API error: {e.response.text}"}
            except Exception as e:
                return {"error": True, "status_code": 500, "message": f"An unexpected internal error occurred: {str(e)}"}

    async def get_weather_by_city(self, query: str):
        if query in self.cache:
            return {"error": False, "data": self.cache[query]}

        result = await self._fetch_from_api("weather", {"q": query})
        if not result["error"]:
            self.cache[query] = result["data"]
        return result

    async def get_forecast_by_city(self, query: str, days: int = 5):
        cache_key = f"forecast_{query}"
        if cache_key in self.cache:
            return {"error": False, "data": self.cache[cache_key]}

        result = await self._fetch_from_api("forecast", {"q": query})
        if not result["error"]:
            raw_list = result["data"].get("list", [])
            processed = []
            for item in raw_list[:days]:
                processed.append({
                    "date": item.get("dt_txt", "N/A"),
                    "temperature": item.get("main", {}).get("temp", 0),
                    "description": item.get("weather", [{}])[0].get("description", "N/A")
                })
            self.cache[cache_key] = processed
            return {"error": False, "data": processed}
        return result