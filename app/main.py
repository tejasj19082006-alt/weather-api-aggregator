from fastapi import FastAPI

# This is the "app" that uvicorn is looking for!
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Weather API is officially running!"}