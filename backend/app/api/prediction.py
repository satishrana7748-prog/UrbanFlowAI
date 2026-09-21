from fastapi import APIRouter
import pandas as pd
import os
from xgboost import XGBRegressor


router = APIRouter(
    prefix="/prediction",
    tags=["Traffic Prediction"]
)


# =========================
# File Paths
# =========================

DATA_FILE = r"D:\UrbanFlowAI\data\traffic.csv"

MODEL_FILE = r"D:\UrbanFlowAI\ai\models\traffic_xgboost_model.json"


# =========================
# Load Model
# =========================

model = XGBRegressor()

model.load_model(MODEL_FILE)


# =========================
# Traffic Forecast API
# =========================

@router.get("/forecast")
def traffic_forecast():

    df = pd.read_csv(DATA_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Get latest record for every junction
    latest_data = (
        df.sort_values("timestamp")
        .groupby("junction")
        .tail(1)
        .copy()
    )

    predictions = []

    for _, row in latest_data.iterrows():

        current_vehicle_count = int(row["vehicle_count"])

        current_speed = float(row["average_speed_kmph"])

        current_time = row["timestamp"]

        # Prediction time = 15 minutes ahead
        future_time = current_time + pd.Timedelta(minutes=15)

        features = pd.DataFrame([
            {
                "vehicle_count": current_vehicle_count,
                "average_speed_kmph": current_speed,
                "hour": future_time.hour,
                "minute": future_time.minute
            }
        ])

        predicted_count = model.predict(features)[0]

        predicted_count = max(0, round(float(predicted_count)))

        # Determine predicted congestion
        if predicted_count >= 200:
            predicted_congestion = "Very High"
        elif predicted_count >= 150:
            predicted_congestion = "High"
        elif predicted_count >= 100:
            predicted_congestion = "Medium"
        else:
            predicted_congestion = "Low"

        predictions.append(
            {
                "junction": row["junction"],
                "current_vehicle_count": current_vehicle_count,
                "current_speed_kmph": current_speed,
                "predicted_vehicle_count_15_min": predicted_count,
                "predicted_congestion": predicted_congestion
            }
        )

    return {
        "status": "success",
        "prediction_type": "XGBoost ML Prediction",
        "total_junctions": len(predictions),
        "predictions": predictions
    }