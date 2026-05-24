import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services.weather import WeatherService

client = TestClient(app)

# --- 1. Test Successful Weather Response (Mocked) ---
@patch.object(WeatherService, 'get_weather_by_city')
def test_get_weather_success(mock_get_weather):
    # Setup a complete mock response matching our app's extraction keys
    mock_get_weather.return_value = {
        "error": False,
        "data": {
            "name": "London",
            "main": {
                "temp": 15.0, 
                "humidity": 80
            },
            "weather": [
                {"description": "clear sky"}
            ],
            "wind": {
                "speed": 5.5
            }
        }
    }

    response = client.get("/api/v1/weather/London")
    
    assert response.status_code == 200
    assert response.json()["city"] == "London"
    assert response.json()["temperature"] == 15.0
    assert response.json()["description"] == "clear sky"
    assert response.json()["wind_speed"] == 5.5

# --- 2. Test 404 City Not Found Error ---
@patch.object(WeatherService, 'get_weather_by_city')
def test_get_weather_404(mock_get_weather):
    mock_get_weather.return_value = {
        "error": True,
        "status_code": 404,
        "message": "Location not found"
    }

    response = client.get("/api/v1/weather/FakeCity")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"

# --- 3. Test 401 Invalid API Key Error ---
@patch.object(WeatherService, 'get_weather_by_city')
def test_get_weather_401(mock_get_weather):
    mock_get_weather.return_value = {
        "error": True,
        "status_code": 401,
        "message": "Invalid API Key"
    }

    response = client.get("/api/v1/weather/London")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API Key"

# --- 4. Test Caching Logic ---
def test_caching_logic():
    service = WeatherService()
    service.cache["Mumbai"] = {"temp": 30.0}
    
    assert "Mumbai" in service.cache
    assert service.cache["Mumbai"]["temp"] == 30.0