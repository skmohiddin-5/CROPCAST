import requests
import joblib
import pandas as pd

# --------------------------------------------------
# 1. Location coordinates
# --------------------------------------------------

latitude = 16.5062
longitude = 80.6480

# --------------------------------------------------
# 2. Get live weather
# --------------------------------------------------

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m",
    "timezone": "auto"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Weather API request failed.")
    exit()

weather = response.json()["current"]

# --------------------------------------------------
# 3. Extract weather values
# --------------------------------------------------

temperature = weather["temperature_2m"]
humidity = weather["relative_humidity_2m"]
pressure = weather["surface_pressure"]
wind_speed = weather["wind_speed_10m"]

print("\n===== LIVE WEATHER =====")
print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Pressure:", pressure, "hPa")
print("Wind Speed:", wind_speed, "km/h")

# --------------------------------------------------
# 4. Load ML model
# --------------------------------------------------

model = joblib.load("models/rainfall_model.pkl")

# --------------------------------------------------
# 5. Prepare data for model
# --------------------------------------------------

# We don't yet have today's rainfall from the API,
# so temporarily use 0.
rain_today = 0

weather_data = pd.DataFrame([{
    "Temperature": temperature,
    "Humidity": humidity,
    "Pressure": pressure,
    "WindSpeed": wind_speed,
    "RainToday": rain_today
}])

# --------------------------------------------------
# 6. Make prediction
# --------------------------------------------------

prediction = model.predict(weather_data)[0]

probabilities = model.predict_proba(weather_data)[0]

rain_probability = probabilities[1] * 100

# --------------------------------------------------
# 7. Display result
# --------------------------------------------------

print("\n===== RAINFALL PREDICTION =====")

if prediction == 1:
    print("Rain predicted")
else:
    print("No rain predicted")

print(f"Rain probability: {rain_probability:.2f}%")