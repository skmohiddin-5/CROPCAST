import requests
import joblib
import pandas as pd

# -----------------------------------------
# 1. Get village name
# -----------------------------------------

place = input("Enter village/city name: ")

# -----------------------------------------
# 2. Find coordinates
# -----------------------------------------

geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

geocoding_params = {
    "name": place,
    "count": 1,
    "language": "en",
    "format": "json",
    "countryCode": "IN"
}

response = requests.get(
    geocoding_url,
    params=geocoding_params
)

if response.status_code != 200:
    print("Location search failed.")
    exit()

location_data = response.json()

if "results" not in location_data:
    print("Location not found.")
    exit()

location = location_data["results"][0]

latitude = location["latitude"]
longitude = location["longitude"]

print("\nLocation found:")
print(location["name"])
print(location.get("admin1", ""))
print(location.get("country", ""))

# -----------------------------------------
# 3. Get live weather
# -----------------------------------------

weather_url = "https://api.open-meteo.com/v1/forecast"

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

response = requests.get(
    weather_url,
    params=weather_params
)

if response.status_code != 200:
    print("Weather request failed.")
    exit()

weather = response.json()["current"]

temperature = weather["temperature_2m"]
humidity = weather["relative_humidity_2m"]
pressure = weather["surface_pressure"]
wind_speed = weather["wind_speed_10m"]
precipitation = weather["precipitation"]

print("\n===== LIVE WEATHER =====")
print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Pressure:", pressure, "hPa")
print("Wind Speed:", wind_speed, "km/h")
print("Precipitation:", precipitation, "mm")

# -----------------------------------------
# 4. Load ML model
# -----------------------------------------

model = joblib.load("models/rainfall_model.pkl")

# -----------------------------------------
# 5. Prepare model input
# -----------------------------------------

weather_data = pd.DataFrame([{
    "Temperature": temperature,
    "Humidity": humidity,
    "Pressure": pressure,
    "WindSpeed": wind_speed,
    "RainToday": 1 if precipitation > 0 else 0
}])

# -----------------------------------------
# 6. Predict rainfall
# -----------------------------------------

prediction = model.predict(weather_data)[0]

probabilities = model.predict_proba(weather_data)[0]

rain_probability = probabilities[1] * 100

# -----------------------------------------
# 7. Display result
# -----------------------------------------

print("\n===== RAINFALL PREDICTION =====")

if prediction == 1:
    print("Rain predicted")
else:
    print("No rain predicted")

print(f"Rain probability: {rain_probability:.2f}%")