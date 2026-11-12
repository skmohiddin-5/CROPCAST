from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path
import requests
import joblib
import pandas as pd
from gtts import gTTS

from backend.database import (
    create_database,
    save_prediction,
    get_prediction_history
)


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Smart Rainfall Prediction System",
    description="Predict rainfall using live weather data",
    version="1.0"
)

create_database()


# --------------------------------------------------
# Load trained ML model
# --------------------------------------------------

model = joblib.load("models/rainfall_model.pkl")

AUDIO_FOLDER = Path("audio")
AUDIO_FOLDER.mkdir(exist_ok=True)


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get("/")
def home():

    frontend_path = (
        Path(__file__).parent.parent
        / "frontend"
        / "index.html"
    )

    return FileResponse(frontend_path)


# --------------------------------------------------
# Rainfall prediction
# --------------------------------------------------

@app.get("/predict")
def predict(village: str, language: str = "en"):

    # 1. Find village coordinates

    geocoding_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    geocoding_params = {
        "name": village,
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "IN"
    }

    try:
        response = requests.get(
            geocoding_url,
            params=geocoding_params,
            timeout=15
        )
        response.raise_for_status()
        location_data = response.json()

    except requests.RequestException:
        return {
            "error": "Location search failed. Please try again."
        }

    if not location_data.get("results"):
        return {
            "error": "Village not found. Please enter a valid location."
        }

    location = location_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]


    # 2. Get live weather

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "surface_pressure,"
            "wind_speed_10m,"
            "precipitation"
        ),
        "timezone": "auto"
    }

    try:
        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=15
        )
        response.raise_for_status()
        weather_response = response.json()

        weather = weather_response["current"]

    except (requests.RequestException, KeyError, TypeError):
        return {
            "error": "Weather data is unavailable. Please try again."
        }


    # 3. Extract weather information

    temperature = weather["temperature_2m"]
    humidity = weather["relative_humidity_2m"]
    pressure = weather["surface_pressure"]
    wind_speed = weather["wind_speed_10m"]
    precipitation = weather["precipitation"]


    # 4. Determine whether it is raining

    rain_today = 1 if precipitation > 0 else 0


    # 5. Prepare data for ML model

    weather_data = pd.DataFrame([{
        "Temperature": temperature,
        "Humidity": humidity,
        "Pressure": pressure,
        "WindSpeed": wind_speed,
        "RainToday": rain_today
    }])


    # 6. Make rainfall prediction

    prediction = model.predict(weather_data)[0]

    probabilities = model.predict_proba(weather_data)[0]

    rain_probability = float(probabilities[1] * 100)


    # 7. Create translated prediction text

    if language == "te":

        if prediction == 1:
            prediction_text = "వర్షం పడే అవకాశం ఉంది"
        else:
            prediction_text = "వర్షం పడే అవకాశం తక్కువగా ఉంది"

    elif language == "hi":

        if prediction == 1:
            prediction_text = "बारिश होने की संभावना है"
        else:
            prediction_text = "बारिश होने की संभावना कम है"

    else:

        if prediction == 1:
            prediction_text = "Rain predicted"
        else:
            prediction_text = "No rain predicted"


    # 8. Create voice notification

    if language == "te":

        if prediction == 1:
            voice_text = (
                f"{location['name']} ప్రాంతంలో వర్షం పడే అవకాశం ఉంది. "
                f"వర్షం పడే అవకాశం {rain_probability:.0f} శాతం."
            )
        else:
            voice_text = (
                f"{location['name']} ప్రాంతంలో వర్షం పడే అవకాశం తక్కువగా ఉంది. "
                f"వర్షం పడే అవకాశం {rain_probability:.0f} శాతం."
            )

        voice_language = "te"

    elif language == "hi":

        if prediction == 1:
            voice_text = (
                f"{location['name']} क्षेत्र में बारिश होने की संभावना है। "
                f"बारिश की संभावना {rain_probability:.0f} प्रतिशत है।"
            )
        else:
            voice_text = (
                f"{location['name']} क्षेत्र में बारिश होने की संभावना कम है। "
                f"बारिश की संभावना {rain_probability:.0f} प्रतिशत है।"
            )

        voice_language = "hi"

    else:

        if prediction == 1:
            voice_text = (
                f"There is a chance of rain in {location['name']}. "
                f"The probability of rain is {rain_probability:.0f} percent."
            )
        else:
            voice_text = (
                f"There is a low chance of rain in {location['name']}. "
                f"The probability of rain is {rain_probability:.0f} percent."
            )

        voice_language = "en"


    # Generate voice file.
    # Prediction can still be returned if TTS temporarily fails.

    voice_status = "success"

    try:
        tts = gTTS(
            text=voice_text,
            lang=voice_language
        )

        tts.save(str(AUDIO_FOLDER / "rainfall_alert.mp3"))

    except Exception:
        voice_status = "failed"


    # 9. Save prediction in SQLite

    save_prediction(
        village=location["name"],
        state=location.get("admin1", ""),
        country=location.get("country", ""),
        latitude=latitude,
        longitude=longitude,
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        wind_speed=wind_speed,
        precipitation=precipitation,
        rain_probability=rain_probability,
        prediction=prediction_text,
        language=language
    )


    # 10. Return prediction

    return {
        "location": location["name"],
        "state": location.get("admin1", ""),
        "country": location.get("country", ""),
        "latitude": latitude,
        "longitude": longitude,
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "precipitation": precipitation
        },
        "prediction": (
            "Rain predicted"
            if prediction == 1
            else "No rain predicted"
        ),
        "prediction_text": prediction_text,
        "rain_probability": round(rain_probability, 2),
        "voice_status": voice_status
    }


# --------------------------------------------------
# Voice alert endpoint
# --------------------------------------------------

@app.get("/voice-alert")
def voice_alert():

    audio_path = AUDIO_FOLDER / "rainfall_alert.mp3"

    if not audio_path.exists():
        return {
            "error": "Voice alert has not been generated yet."
        }

    return FileResponse(
        audio_path,
        media_type="audio/mpeg"
    )


# --------------------------------------------------
# Prediction history endpoint
# --------------------------------------------------

@app.get("/history")
def prediction_history():

    return get_prediction_history()