from pydantic import BaseModel
from typing import List, Optional

class WeatherResponse(BaseModel):
    city: str
    state: Optional[str] = None
    temperature: float
    humidity: int
    description: str
    wind_speed: float

class DailyForecast(BaseModel):
    date: str
    temperature: float
    description: str

class ForecastResponse(BaseModel):
    city: str
    state: Optional[str] = None
    forecast_days: int
    forecasts: List[DailyForecast]