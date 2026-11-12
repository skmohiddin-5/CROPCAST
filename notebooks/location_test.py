import requests

# -----------------------------------------
# Ask user for location
# -----------------------------------------

place = input("Enter village/city name: ")

# -----------------------------------------
# Open-Meteo Geocoding API
# -----------------------------------------

url = "https://geocoding-api.open-meteo.com/v1/search"

params = {
    "name": place,
    "count": 5,
    "language": "en",
    "format": "json"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Location search failed.")
    exit()

data = response.json()

# -----------------------------------------
# Check whether location was found
# -----------------------------------------

if "results" not in data:
    print("Location not found.")
    exit()

print("\n===== LOCATIONS FOUND =====")

for location in data["results"]:
    print(
        location["name"],
        "|",
        location.get("admin1", ""),
        "|",
        location.get("country", ""),
        "|",
        location["latitude"],
        location["longitude"]
    )