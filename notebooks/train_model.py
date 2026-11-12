import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv("dataset/rain_forecasting.csv")


# --------------------------------------------------
# 2. Create API-compatible features
# --------------------------------------------------

df["Temperature"] = (
    df["MinTemp"] + df["MaxTemp"]
) / 2

df["Humidity"] = (
    df["Humidity9am"] + df["Humidity3pm"]
) / 2

df["Pressure"] = (
    df["Pressure9am"] + df["Pressure3pm"]
) / 2

df["WindSpeed"] = (
    df["WindSpeed9am"] + df["WindSpeed3pm"]
) / 2


# --------------------------------------------------
# 3. Select features and target
# --------------------------------------------------

features = [
    "Temperature",
    "Humidity",
    "Pressure",
    "WindSpeed",
    "RainToday"
]

X = df[features].copy()

y = df["RainTomorrow"].map({
    "Yes": 1,
    "No": 0
})


# --------------------------------------------------
# 4. Convert RainToday
# --------------------------------------------------

X["RainToday"] = X["RainToday"].map({
    "Yes": 1,
    "No": 0
})


# --------------------------------------------------
# 5. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# --------------------------------------------------
# 6. Create Random Forest
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# --------------------------------------------------
# 7. Train
# --------------------------------------------------

model.fit(X_train, y_train)


# --------------------------------------------------
# 8. Save model
# --------------------------------------------------

joblib.dump(
    model,
    "models/rainfall_model.pkl"
)

print("\nModel saved successfully!")


# --------------------------------------------------
# 9. Predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 10. Evaluation
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n===== MODEL ACCURACY =====")
print(f"Accuracy: {accuracy * 100:.2f}%")


print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, y_pred))


print("\n===== CONFUSION MATRIX =====")
print(confusion_matrix(y_test, y_pred))