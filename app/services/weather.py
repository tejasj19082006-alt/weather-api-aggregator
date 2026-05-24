import os
import httpx
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        # Cache for 10 minutes (600 seconds), max 100 entries
        self.cache = TTLCache(maxsize=100, ttl=600)

    async def _fetch_from_api(self, endpoint: str, params: dict):
        """Helper to handle HTTP requests safely."""
        params["appid"] = self.api_key
        params["units"] = "metric"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/{endpoint}", params=params)
                if response.status_code != 200:
                    return {"error": True, "status_code": response.status_code, "message": "External API error"}
                return {"error": False, "data": response.json()}
            except Exception as e:
                return {"error": True, "status_code": 500, "message": str(e)}

    async def get_weather_by_city(self, query: str):
        if query in self.cache:
            return {"error": False, "data": self.cache[query]}

        result = await self._fetch_from_api("weather", {"q": query})
        if not result["error"]:
            self.cache[query] = result["data"]
        return result

    async def get_forecast_by_city(self, query: str, days: int = 5):
        # Forecasts are complex, caching the raw result
        cache_key = f"forecast_{query}"
        if cache_key in self.cache:
            return {"error": False, "data": self.cache[cache_key]}

        result = await self._fetch_from_api("forecast", {"q": query})
        if not result["error"]:
            # Basic processing: simplify forecast to 5 entries
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