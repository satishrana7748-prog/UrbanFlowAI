import pandas as pd
import os


# ============================================================
# URBANFLOW AI
# Prepare 15-Minute Traffic Prediction Dataset
# IS-8: Predictive Traffic Management
# ============================================================

INPUT_FILE = r"D:\UrbanFlowAI\data\traffic_history.csv"

OUTPUT_FILE = r"D:\UrbanFlowAI\data\traffic_15min_dataset.csv"


# ============================================================
# 1. Load Historical Dataset
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("URBANFLOW AI - 15 MINUTE DATASET PREPARATION")
print("=" * 70)

print("Historical records:", len(df))


# ============================================================
# 2. Prepare Timestamp
# ============================================================

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values(
    ["timestamp", "junction"]
).reset_index(drop=True)


# ============================================================
# 3. Create Snapshot ID
# ============================================================

unique_timestamps = sorted(
    df["timestamp"].unique()
)

timestamp_to_snapshot = {
    timestamp: index
    for index, timestamp in enumerate(unique_timestamps)
}

df["snapshot_id"] = df["timestamp"].map(
    timestamp_to_snapshot
)


print("Total snapshots:", len(unique_timestamps))
print("Junctions:", df["junction"].nunique())


# ============================================================
# 4. Create 15-Minute Future Target
# ============================================================

# Simulator generates one snapshot every 5 seconds.
#
# 15 minutes = 900 seconds
# 900 / 5 = 180 snapshots

FUTURE_STEPS = 180

df["future_vehicle_count_15min"] = (
    df.groupby("junction")["vehicle_count"]
    .shift(-FUTURE_STEPS)
)


# ============================================================
# 5. Remove Rows Without Future Target
# ============================================================

before = len(df)

df = df.dropna(
    subset=["future_vehicle_count_15min"]
).copy()

after = len(df)


# ============================================================
# 6. Create Time Features
# ============================================================

df["hour"] = df["timestamp"].dt.hour

df["minute"] = df["timestamp"].dt.minute


# ============================================================
# 7. Clean Future Target
# ============================================================

df["future_vehicle_count_15min"] = (
    df["future_vehicle_count_15min"]
    .astype(int)
)


# ============================================================
# 8. Select Final ML Columns
# ============================================================

final_columns = [
    "timestamp",
    "junction",
    "vehicle_count",
    "average_speed_kmph",
    "utilization_percent",
    "congestion_level",
    "hour",
    "minute",
    "future_vehicle_count_15min"
]

df = df[final_columns]


# ============================================================
# 9. Save Dataset
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 10. Dataset Information
# ============================================================

print()
print("Dataset preparation completed.")
print("Records before:", before)
print("Records after :", after)

print()
print("Output file:")
print(OUTPUT_FILE)

print()
print("Sample:")
print(df.head(10).to_string(index=False))

print()
print("=" * 70)
