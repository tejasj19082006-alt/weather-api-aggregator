from fastapi import FastAPI
import os
from dotenv import load_dotenv

# 1. Load the environment variables from the .env file
load_dotenv()

# 2. Fetch the API key securely
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 3. Initialize the app
app = FastAPI()
from fastapi.responses import Response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 means "No Content" - it just tells the browser to stop asking.
@app.get("/")
def home():
    # 4. We check if the key loaded successfully. 
    # We only print the first 5 characters for security!
    if API_KEY:
        masked_key = f"{API_KEY[:5]}...[HIDDEN]"
        return {
            "status": "Success",
            "message": "Weather API Aggregator is Live!",
            "api_key_status": "Loaded correctly",
            "masked_key": masked_key
        }
    else:
        return {
            "status": "Warning",
            "message": "Weather API Aggregator is Live!",
            "api_key_status": "MISSING. Check your .env file."
        }