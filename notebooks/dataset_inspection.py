import pandas as pd


file_path = "dataset/rain_forecasting.csv"

df = pd.read_csv(file_path)

# --------------------------------------------------
# 2. Basic information
# --------------------------------------------------

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())