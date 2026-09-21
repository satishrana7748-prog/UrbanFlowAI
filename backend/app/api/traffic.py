from fastapi import APIRouter
import csv
import os

router = APIRouter(
    prefix="/traffic",
    tags=["Traffic"]
)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "data",
    "traffic.csv"
)


@router.get("/status")
def traffic_status():

    traffic_records = []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            traffic_records.append({
                "timestamp": row["timestamp"],
                "junction": row["junction"],
                "vehicle_count": int(row["vehicle_count"]),
                "average_speed_kmph": float(row["average_speed_kmph"]),
                "congestion_level": row["congestion_level"]
            })

    return {
        "status": "success",
        "total_records": len(traffic_records),
        "data": traffic_records
    }