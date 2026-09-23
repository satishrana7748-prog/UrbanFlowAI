import random
import time
import json
import csv
import os
from datetime import datetime


# ============================================================
# URBANFLOW AI - TRAFFIC SIMULATOR V2
# ============================================================

JUNCTIONS = {
    "J1": {
        "name": "Main Market",
        "capacity": 300,
        "base_demand": 0.55
    },
    "J2": {
        "name": "Railway Square",
        "capacity": 350,
        "base_demand": 0.65
    },
    "J3": {
        "name": "City Center",
        "capacity": 400,
        "base_demand": 0.85
    },
    "J4": {
        "name": "University Road",
        "capacity": 300,
        "base_demand": 0.50
    },
    "J5": {
        "name": "Hospital Road",
        "capacity": 280,
        "base_demand": 0.70
    },
    "J6": {
        "name": "Airport Road",
        "capacity": 350,
        "base_demand": 0.60
    }
}


def get_time_factor(hour):
    """
    Traffic demand changes according to time of day.
    """

    # Morning peak
    if 8 <= hour < 10:
        return 1.35

    # Midday
    if 10 <= hour < 16:
        return 0.95

    # Evening peak
    if 16 <= hour < 19:
        return 1.40

    # Evening normal
    if 19 <= hour < 22:
        return 1.05

    # Night
    return 0.45


def get_congestion_level(utilization, average_speed):
    """
    Determine congestion using road utilization
    and average speed.
    """

    if utilization >= 0.90 or average_speed < 15:
        return "HIGH"

    if utilization >= 0.60 or average_speed < 30:
        return "MEDIUM"

    return "LOW"


def calculate_speed(utilization):
    """
    Calculate realistic average speed from traffic utilization.

    Higher utilization -> lower speed.
    """

    if utilization < 0.40:
        speed = random.uniform(40, 50)

    elif utilization < 0.60:
        speed = random.uniform(30, 40)

    elif utilization < 0.80:
        speed = random.uniform(20, 30)

    elif utilization < 1.00:
        speed = random.uniform(12, 22)

    else:
        speed = random.uniform(6, 15)

    return round(speed, 2)


def generate_traffic_state():
    """
    Generate one realistic traffic snapshot.
    """

    current_time = datetime.now()

    hour = current_time.hour

    time_factor = get_time_factor(hour)

    traffic_data = []

    for junction_id, config in JUNCTIONS.items():

        capacity = config["capacity"]
        base_demand = config["base_demand"]

        # ----------------------------------------------------
        # Calculate traffic demand
        # ----------------------------------------------------

        demand = base_demand * time_factor

        # Small natural variation
        variation = random.uniform(0.90, 1.10)

        demand = demand * variation

        # ----------------------------------------------------
        # Calculate vehicle count
        # ----------------------------------------------------

        vehicle_count = int(capacity * demand)

        # Keep value within realistic range
        vehicle_count = max(
            20,
            min(vehicle_count, int(capacity * 1.20))
        )

        # ----------------------------------------------------
        # Road utilization
        # ----------------------------------------------------

        utilization = vehicle_count / capacity

        # ----------------------------------------------------
        # Calculate speed from utilization
        # ----------------------------------------------------

        average_speed = calculate_speed(utilization)

        # ----------------------------------------------------
        # Congestion
        # ----------------------------------------------------

        congestion_level = get_congestion_level(
            utilization,
            average_speed
        )

        traffic_data.append({

            "junction": junction_id,

            "junction_name": config["name"],

            "vehicle_count": vehicle_count,

            "road_capacity": capacity,

            "utilization_percent": round(
                utilization * 100,
                1
            ),

            "average_speed_kmph": average_speed,

            "congestion_level": congestion_level
        })

    return {

        "timestamp": current_time.isoformat(),

        "hour": hour,

        "traffic_period": get_traffic_period(hour),

        "total_junctions": len(JUNCTIONS),

        "traffic": traffic_data
    }

def save_traffic_state(data):
    """
    Save latest simulated traffic state
    so that other UrbanFlow AI modules can use it.
    """

    output_file = r"D:\UrbanFlowAI\data\live_traffic.json"

    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)

    return output_file

def save_historical_traffic(data):
    """
    Append every traffic snapshot to historical CSV dataset.
    """

    output_file = r"D:\UrbanFlowAI\data\traffic_history.csv"

    file_exists = os.path.exists(output_file)

    with open(
        output_file,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        # Create header only once
        if not file_exists:
            writer.writerow([
                "timestamp",
                "junction",
                "junction_name",
                "vehicle_count",
                "road_capacity",
                "utilization_percent",
                "average_speed_kmph",
                "congestion_level"
            ])

        # Save every junction
        for traffic in data["traffic"]:

            writer.writerow([
                data["timestamp"],
                traffic["junction"],
                traffic["junction_name"],
                traffic["vehicle_count"],
                traffic["road_capacity"],
                traffic["utilization_percent"],
                traffic["average_speed_kmph"],
                traffic["congestion_level"]
            ])

    return output_file

def get_traffic_period(hour):
    """
    Return human-readable traffic period.
    """

    if 8 <= hour < 10:
        return "MORNING_PEAK"

    if 10 <= hour < 16:
        return "MIDDAY"

    if 16 <= hour < 19:
        return "EVENING_PEAK"

    if 19 <= hour < 22:
        return "EVENING"

    return "NIGHT"


def print_traffic_state(data):

    print("\n" + "=" * 90)

    print(
        "                 URBANFLOW AI - LIVE TRAFFIC SIMULATOR V2"
    )

    print("=" * 90)

    print(f"Timestamp      : {data['timestamp']}")

    print(f"Traffic Period : {data['traffic_period']}")

    print(f"Junctions      : {data['total_junctions']}")

    print("-" * 90)

    print(
        f"{'ID':<5}"
        f"{'Junction':<20}"
        f"{'Vehicles':<12}"
        f"{'Capacity':<12}"
        f"{'Utilization':<14}"
        f"{'Speed(km/h)':<15}"
        f"{'Congestion'}"
    )

    print("-" * 90)

    for junction in data["traffic"]:

        print(
            f"{junction['junction']:<5}"
            f"{junction['junction_name']:<20}"
            f"{junction['vehicle_count']:<12}"
            f"{junction['road_capacity']:<12}"
            f"{str(junction['utilization_percent'])+'%':<14}"
            f"{str(junction['average_speed_kmph']) + 'km/h':<15}"
            f"{junction['congestion_level']}"
        )

    print("=" * 90)


def run_simulator():

    print()
    print("Starting UrbanFlow AI Traffic Simulator V2...")
    print("Realistic traffic-demand simulation enabled.")
    print("Press CTRL+C to stop.\n")

    try:

        while True:

            traffic_state = generate_traffic_state()

            save_traffic_state(traffic_state)

            save_historical_traffic(traffic_state)

            print_traffic_state(traffic_state)

            time.sleep(5)

    except KeyboardInterrupt:

        print("\nTraffic simulator stopped.")


if __name__ == "__main__":
    run_simulator()