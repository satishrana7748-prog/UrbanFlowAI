import pandas as pd
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib


# =========================
# 1. Load Dataset
# =========================

DATA_FILE = r"D:\UrbanFlowAI\data\traffic.csv"

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully")
print("Total records:", len(df))


# =========================
# 2. Prepare Features
# =========================

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["hour"] = df["timestamp"].dt.hour
df["minute"] = df["timestamp"].dt.minute

X = df[
    [
        "vehicle_count",
        "average_speed_kmph",
        "hour",
        "minute"
    ]
]

y = df["vehicle_count"]


# =========================
# 3. Split Dataset
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================
# 4. Train XGBoost Model
# =========================

model = XGBRegressor(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)


# =========================
# 5. Evaluate Model
# =========================

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("Model training completed")
print("Mean Absolute Error:", round(mae, 2))


# =========================
# 6. Save Model
# =========================

MODEL_DIR = r"D:\UrbanFlowAI\ai\models"

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "traffic_xgboost_model.json"
)

model.save_model(MODEL_FILE)

print("Model saved successfully")
print("Model path:", MODEL_FILE)