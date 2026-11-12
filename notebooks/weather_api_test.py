import requests

# Example location: Vijayawada
latitude = 16.5062
longitude = 80.6480

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m",
    "timezone": "auto"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

data = response.json()

print("\n===== LIVE WEATHER =====")
print("Temperature:", data["current"]["temperature_2m"], "°C")
print("Humidity:", data["current"]["relative_humidity_2m"], "%")
print("Pressure:", data["current"]["surface_pressure"], "hPa")
print("Wind Speed:", data["current"]["wind_speed_10m"], "km/h")