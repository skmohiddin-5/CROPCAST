import pandas as pd

# Load dataset
df = pd.read_csv("dataset/rain_forecasting.csv")

# --------------------------------------------------
# Create API-compatible features
# --------------------------------------------------

# Average minimum and maximum temperature
df["Temperature"] = (df["MinTemp"] + df["MaxTemp"]) / 2

# Average morning and afternoon humidity
df["Humidity"] = (
    df["Humidity9am"] + df["Humidity3pm"]
) / 2

# Average morning and afternoon pressure
df["Pressure"] = (
    df["Pressure9am"] + df["Pressure3pm"]
) / 2

# Average morning and afternoon wind speed
df["WindSpeed"] = (
    df["WindSpeed9am"] + df["WindSpeed3pm"]
) / 2

# --------------------------------------------------
# Select final features
# --------------------------------------------------

features = [
    "Temperature",
    "Humidity",
    "Pressure",
    "WindSpeed",
    "RainToday"
]

target = "RainTomorrow"

X = df[features].copy()

y = df[target].map({
    "Yes": 1,
    "No": 0
})

# Convert RainToday to 0/1
X["RainToday"] = X["RainToday"].map({
    "Yes": 1,
    "No": 0
})

# --------------------------------------------------
# Display processed data
# --------------------------------------------------

print("\n===== FINAL FEATURES =====")
print(X.head())

print("\n===== FEATURE DATA TYPES =====")
print(X.dtypes)

print("\n===== TARGET =====")
print(y.head())

print("\n===== TARGET DISTRIBUTION =====")
print(y.value_counts())