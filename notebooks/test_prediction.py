import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/rainfall_model.pkl")

# Example live weather data
weather_data = pd.DataFrame([{
    "Temperature": 30.0,
    "Humidity": 80.0,
    "Pressure": 1004.0,
    "WindSpeed": 15.0,
    "RainToday": 1
}])

# Make prediction
prediction = model.predict(weather_data)[0]

# Get probability
probabilities = model.predict_proba(weather_data)[0]

rain_probability = probabilities[1] * 100

print("\n===== RAINFALL PREDICTION =====")

if prediction == 1:
    print("Rain predicted")
else:
    print("No rain predicted")

print(f"Rain probability: {rain_probability:.2f}%")