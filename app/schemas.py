from pydantic import BaseModel, Field
from typing import List

# --- Weather Schemas ---

class WeatherResponse(BaseModel):
    city: str = Field(..., example="Mumbai", description="Name of the requested city")
    temperature: float = Field(..., example=29.5, description="Current temperature in Celsius")
    humidity: int = Field(..., example=62, description="Humidity percentage")
    description: str = Field(..., example="few clouds", description="Brief weather condition")
    wind_speed: float = Field(..., example=4.12, description="Wind speed in meters per second")

# --- Forecast Schemas ---

class DailyForecast(BaseModel):
    date: str = Field(..., example="2024-05-25", description="Date of the forecast")
    temperature: float = Field(..., example=31.0, description="Forecasted temperature")
    description: str = Field(..., example="clear sky", description="Forecasted condition")

class ForecastResponse(BaseModel):
    city: str = Field(..., example="Mumbai")
    forecast_days: int = Field(..., example=5, description="Number of days in the forecast")
    forecasts: List[DailyForecast]